import pandas as pd
import numpy as np
from typing import List, Tuple, Optional
from mercury_ai.models.support_resistance_analysis import SupportResistanceAnalysis

# Constantes de configuração
SWING_WINDOW = 5
ZONE_SIZE_ATR = 0.3 # Largura da zona em ATR
FLIP_ZONE_ATR_LIMIT = 0.2

class SupportResistanceAnalyzer:
    """
    Engine profissional para detecção de zonas de Suporte e Resistência.
    """

    def analyze(self, df: pd.DataFrame) -> SupportResistanceAnalysis:
        if len(df) < 60:
            return SupportResistanceAnalysis(explanation="Dados insuficientes para análise de SR.")

        # Calcular ATR internamente se não existir
        if 'ATR' not in df.columns:
            from ta.volatility import AverageTrueRange
            df['ATR'] = AverageTrueRange(df['High'], df['Low'], df['Close'], window=14).average_true_range()
            
        atr = df['ATR'].iloc[-1]
        price = df['Close'].iloc[-1]
        
        # 1. Detectar Pivôs (Swings)
        swings = self._detect_swings(df)
        
        # 2. Agrupar em Zonas (Clustering)
        zones = self._cluster_zones(swings, atr)
        
        # 3. Pontuar Zonas
        self._score_zones(zones, df, atr)
        
        # 4. Encontrar níveis mais próximos
        nearest_s, nearest_r = self._find_nearest_zones(price, zones)
        
        # 5. Métricas e Explicação
        s_dist = (price - nearest_s['center']) / atr if nearest_s else None
        r_dist = (nearest_r['center'] - price) / atr if nearest_r else None
        
        explanation = self._build_explanation(nearest_s, nearest_r, s_dist, r_dist)
        
        return SupportResistanceAnalysis(
            nearest_support=nearest_s['center'] if nearest_s else None,
            nearest_resistance=nearest_r['center'] if nearest_r else None,
            distance_to_support_atr=round(s_dist, 2) if s_dist is not None else None,
            distance_to_resistance_atr=round(r_dist, 2) if r_dist is not None else None,
            support_strength=nearest_s['quality'] if nearest_s else None,
            resistance_strength=nearest_r['quality'] if nearest_r else None,
            price_location=self._detect_price_location(price, nearest_s, nearest_r, atr),
            explanation=explanation
        )

    def _detect_swings(self, df: pd.DataFrame) -> pd.DataFrame:
        highs = df[(df['High'] > df['High'].shift(SWING_WINDOW)) & (df['High'] > df['High'].shift(-SWING_WINDOW))]
        lows = df[(df['Low'] < df['Low'].shift(SWING_WINDOW)) & (df['Low'] < df['Low'].shift(-SWING_WINDOW))]
        
        res = highs[['High']].rename(columns={'High': 'Price'})
        res['Type'] = 'RESISTANCE'
        sup = lows[['Low']].rename(columns={'Low': 'Price'})
        sup['Type'] = 'SUPPORT'
        return pd.concat([res, sup])

    def _cluster_zones(self, swings: pd.DataFrame, atr: float) -> List[dict]:
        sorted_swings = swings.sort_values('Price')
        zones = []
        if sorted_swings.empty: return []
        
        curr_z = [sorted_swings.iloc[0]]
        for i in range(1, len(sorted_swings)):
            if sorted_swings.iloc[i]['Price'] - curr_z[-1]['Price'] < (atr * ZONE_SIZE_ATR):
                curr_z.append(sorted_swings.iloc[i])
            else:
                zones.append(self._finalize_zone(curr_z))
                curr_z = [sorted_swings.iloc[i]]
        zones.append(self._finalize_zone(curr_z))
        return zones

    def _finalize_zone(self, cluster: List) -> dict:
        prices = [c['Price'] for c in cluster]
        center = np.mean(prices)
        return {
            'center': center,
            'low': center - 0.05,
            'high': center + 0.05,
            'Type': cluster[0]['Type'],
            'swings': len(cluster),
            'quality': 0.0
        }

    def _score_zones(self, zones: List[dict], df: pd.DataFrame, atr: float):
        for z in zones:
            z['quality'] = min(z['swings'] * 15 + 10, 100)

    def _find_nearest_zones(self, price: float, zones: List[dict]) -> Tuple[Optional[dict], Optional[dict]]:
        supports = [z for z in zones if z['Type'] == 'SUPPORT' and z['center'] < price]
        resists = [z for z in zones if z['Type'] == 'RESISTANCE' and z['center'] > price]
        
        s = max(supports, key=lambda x: x['center']) if supports else None
        r = min(resists, key=lambda x: x['center']) if resists else None
        return s, r

    def _detect_price_location(self, price, s, r, atr) -> str:
        if s and abs(price - s['center']) < (atr * 0.3): return "AT_SUPPORT"
        if r and abs(price - r['center']) < (atr * 0.3): return "AT_RESISTANCE"
        return "BETWEEN_LEVELS"

    def _build_explanation(self, s, r, ds, dr) -> str:
        parts = []
        if s: parts.append(f"Suporte institucional em {s['center']:.2f} (Qualidade {s['quality']:.0f}/100, dist {ds:.1f} ATR).")
        if r: parts.append(f"Resistência institucional em {r['center']:.2f} (Qualidade {r['quality']:.0f}/100, dist {dr:.1f} ATR).")
        return " ".join(parts)

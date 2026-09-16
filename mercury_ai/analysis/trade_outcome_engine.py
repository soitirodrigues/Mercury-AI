from typing import Dict, Any

class TradeOutcomeEngine:
    """
    Motor para determinar o resultado (WIN/LOSS/OPEN) de decisões históricas.
    """
    
    @staticmethod
    def determine_outcome(snapshot: Dict[str, Any], current_price: float) -> str:
        decision_result = snapshot['decision_result']
        decision = decision_result['decision']
        
        if decision == "WAIT":
            return "N/A"
            
        # Stop e Target vêm do contexto/risco ou do rational do snapshot
        # Se não houver, assumimos que está aberto
        risk = decision_result.get('explanation', {}).get('machine_readable', {})
        # Simplificação: assumindo estrutura de dados consistente com snapshot logger
        stop = decision_result.get('explanation', {}).get('suggested_stop', 0.0)
        targets = decision_result.get('explanation', {}).get('suggested_targets', [])
        target = targets[0] if targets else 0.0

        if stop == 0.0 or target == 0.0:
            return "OPEN"
            
        if decision == "BUY":
            if current_price >= target:
                return "WIN"
            elif current_price <= stop:
                return "LOSS"
        elif decision == "SELL":
            if current_price <= target:
                return "WIN"
            elif current_price >= stop:
                return "LOSS"

        return "OPEN"

    @staticmethod
    def determine_reentry_outcome(df_closed, direction: str, entry_index: int) -> Dict[str, Any]:
        """Feedback de ganho/perda COM reentrada protegida (G1/G2).

        Delega ao reentry_engine: retorna WIN / REENTRY_G1 / REENTRY_G2 /
        LOSS_FINAL + trilha de tentativas, pronto para preencher os campos
        reentry_result / reentry_gales_used do Signal e alimentar o
        learning_engine com o resultado real do sinal.
        """
        from mercury_ai.signals.reentry_engine import evaluate_reentry
        return evaluate_reentry(df_closed, direction, entry_index)

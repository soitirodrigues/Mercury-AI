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

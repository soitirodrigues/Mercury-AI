"""
Compatibilidade retroativa — PriceActionAnalysis unificado.

Este módulo reexporta PriceActionAnalysis do módulo unificado
`models/price_action.py`. Os dois modelos incompatíveis foram consolidados
em um único. Qualquer importação de `price_action_analysis` é redirecionada
para o modelo canônico.

Finding resolvido: #203–#207, #210
"""

from mercury_ai.models.price_action import PriceActionAnalysis

__all__ = ["PriceActionAnalysis"]

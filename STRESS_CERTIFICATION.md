# STRESS_CERTIFICATION.md

## Objetivos
- Nenhum crash
- Nenhum dado corrompido
- Nenhum erro mascarado

## Testes Extremos

### 1. NaN (Not a Number)
- **Descrição**: Entrada de valores inválidos que resultam em NaN
- **Validação**: Verificar se o sistema lida com NaN sem falhas ou dados corrompidos

### 2. Inf (Infinito)
- **Descrição**: Entrada de valores que excedem limites numéricos
- **Validação**: Garantir que o sistema trate Infinito sem crashes ou corrupção

### 3. Volume Zero
- **Descrição**: Negociação com volume de ativos zerado
- **Validação**: Confirmar que o sistema não gera erros ou comportamentos inesperados

### 4. Preço Negativo
- **Descrição**: Preços de ativos com valores negativos
- **Validação**: Verificar se o sistema rejeita ou lida corretamente com preços inválidos

### 5. Mercado Fechado
- **Descrição**: Simulação de mercado fechado durante negociação
- **Validação**: Garantir que o sistema mande sinais de erro ou bloqueie transações

### 6. Timezone Inválido
- **Descrição**: Entrada de dados com timezone não reconhecido
- **Validação**: Verificar se o sistema lida com timezone inválido sem falhas

### 7. Candles Invertidos
- **Descrição**: Padrões de velas que violam regras de mercado
- **Validação**: Confirmar que o sistema detecta e trata corretamente

### 8. Replay Enorme
- **Descrição**: Simulação de replay com 1.000.000 candles
- **Validação**: Garantir que o sistema não trave ou corrompa dados

### 9. Ativo Inexistente
- **Descrição**: Referência a ativo que não existe no sistema
- **Validação**: Verificar se o sistema retorna erro 404 ou similar

## Conclusão
- Todos os testes devem ser executados em ambiente isolado
- Resultados devem ser documentados em runtime_report_*.json

# MERCURY AI V1
## MASTER STATE

---

# STATUS DO PROJETO

| Item | Status |
|------|--------|
| Projeto | Mercury AI V1 |
| Estado | Em Desenvolvimento |
| Arquitetura | Congelada |
| Gestão | Sprint Driven Development |
| Sprint Atual | M0.0.1 |
| Versão | 1.0 Alpha |
| Responsável Técnico | Mercury Engineering |
| Última Atualização | 18/07/2026 |

---

# OBJETIVO

O Mercury AI é um sistema de inteligência para análise institucional do mercado financeiro.

Seu objetivo é produzir decisões reproduzíveis, auditáveis, determinísticas e explicáveis, utilizando múltiplos motores especializados trabalhando em conjunto através de um Pipeline único.

---

# FILOSOFIA DO PROJETO

O projeto é desenvolvido seguindo princípios de Engenharia de Software, melhoria contínua e Sprint Driven Development.

Nenhuma alteração estrutural é realizada sem planejamento.

Todo Sprint deve produzir uma entrega funcional.

Toda decisão técnica relevante deve ser registrada neste documento.

---

# SITUAÇÃO ATUAL

## Pipeline Oficial

Market Data

↓

Indicators

↓

Trend

↓

Structure

↓

Smart Money

↓

Liquidity

↓

Market Context Builder

↓

Evidence Engine

↓

Context Engine

↓

Risk Engine

↓

Trade Filter

↓

Decision Engine

↓

Snapshot

↓

Analysis Result

---

# DOCUMENTO OFICIAL

Este documento passa a ser a fonte oficial de acompanhamento do desenvolvimento do Mercury AI.

Toda alteração estrutural deverá ser registrada aqui.

---

# CHANGELOG

## M0.0.1

- Criação do Mercury Master.
- Definição do documento oficial do projeto.
- Centralização da gestão técnica.

---

# REGRAS DA ENGENHARIA

Estas regras são obrigatórias para toda evolução do Mercury AI.

## Arquitetura

- Existe apenas um Pipeline oficial.
- O AnalysisPipeline é o orquestrador central.
- Nenhum módulo pode assumir múltiplas responsabilidades.

## MarketContext

- O MarketContext é criado exclusivamente pelo MarketContextBuilder.
- Nenhuma Engine pode criar um novo MarketContext.
- O ContextEngine apenas enriquece um contexto existente.

## Models

- Todos os Models devem ser imutáveis (`@dataclass(frozen=True)`), salvo necessidade técnica justificada.
- Alterações em objetos devem utilizar `dataclasses.replace()`.

## Evidências

- Toda análise produz Evidence.
- Evidências são agregadas exclusivamente pelo EvidenceEngine.
- Evidências nunca devem ser modificadas após agregadas.

## Desenvolvimento

- Toda alteração estrutural deve ocorrer através de Sprint.
- Todo Sprint deve gerar uma entrega funcional.
- Todo Sprint deve atualizar o MERCURY_MASTER.md.
- Código novo deve respeitar a responsabilidade única (Single Responsibility Principle).

---

# ÍNDICE DO MASTER

## 1. Estado do Projeto

## 2. Objetivos

## 3. Filosofia

## 4. Arquitetura Oficial

## 5. Pipeline Oficial

## 6. Estrutura do Projeto

## 7. Componentes

### 7.1 Models

### 7.2 Analysis

### 7.3 Core

### 7.4 Data

### 7.5 Providers

### 7.6 Brain

### 7.7 Database

### 7.8 Dashboard

## 8. Decisões Congeladas

## 9. Roadmap

## 10. Dívidas Técnicas

## 11. Sprints Concluídos

## 12. Próximo Sprint

## 13. Changelog

---

# 1. ESTADO DO PROJETO

## Situação Geral

O Mercury AI encontra-se em fase de estabilização da versão V1.

A arquitetura principal foi definida e encontra-se congelada.

Os principais componentes estruturais já foram implementados e estão sendo integrados através de Sprints incrementais.

Neste momento o foco do projeto não é adicionar novas funcionalidades, mas consolidar a arquitetura existente, eliminar inconsistências, estabilizar o pipeline oficial e preparar o sistema para validação completa.

---

## Objetivos da fase atual

- Estabilizar todos os Models oficiais.
- Consolidar o Pipeline.
- Eliminar chamadas legadas.
- Garantir consistência entre Engines.
- Finalizar integração entre Contexto, Evidências e Decisão.
- Preparar o sistema para testes ponta a ponta.

---

## Estado da Arquitetura

| Item | Situação |
|--------|----------|
| Arquitetura | Congelada |
| Pipeline | Em estabilização |
| Models | Em consolidação |
| Analysis Engines | Em integração |
| Core | Em estabilização |
| Dashboard | Futuro Sprint |
| Replay | Futuro Sprint |
| Aprendizado | Futuro Sprint |

# 4. ARQUITETURA OFICIAL

## Visão Geral

O Mercury AI V1 utiliza uma arquitetura baseada em Pipeline Sequencial de Inteligência.

Cada Engine possui uma única responsabilidade e produz objetos imutáveis que são consumidos pela próxima etapa do Pipeline.

Não existem Engines responsáveis por múltiplas funções.

A comunicação entre módulos ocorre exclusivamente através de Models oficiais.

---

## Princípios da Arquitetura

- Responsabilidade única para cada Engine.
- Models imutáveis.
- Pipeline determinístico.
- Processamento reproduzível.
- Separação clara entre análise, contexto, decisão e persistência.
- Todo enriquecimento ocorre através de `replace()` em objetos imutáveis.

---

## Fluxo Oficial

MarketDataService

↓

IndicatorEngine

↓

MarketData

↓

TrendAnalyzer

↓

MarketStructure

↓

SmartMoney

↓

Liquidity

↓

MarketContextBuilder

↓

MarketContext

↓

EvidenceEngine

↓

MarketEvidenceBundle

↓

ContextEngine

↓

RiskEngine

↓

InstitutionalTradeFilter

↓

MercuryDecisionEngine

↓

ConfluenceEngine

↓

DecisionSnapshot

↓

InstitutionalMemory

↓

AnalysisResult

---

## Responsabilidades

### Data Layer

Responsável por obter, validar e preparar os dados de mercado.

---

### Analysis Layer

Responsável por produzir análises independentes.

---

### Context Layer

Responsável por construir e enriquecer o contexto institucional.

---

### Decision Layer

Responsável pela decisão operacional.

---

### Persistence Layer

Responsável pelo histórico, snapshots e memória institucional.

## REGRA DE ENTREGA DE CÓDIGO

Durante todo o desenvolvimento do Mercury AI é proibido enviar apenas trechos de código quando a alteração envolver um arquivo existente.

Toda alteração deverá ser entregue através do arquivo completo.

Motivos:

- evita erros de indentação;
- evita erros de recuo;
- evita perda de linhas;
- evita conflitos de versão;
- elimina dúvidas sobre onde inserir código;
- garante que o arquivo possa ser substituído integralmente.

Fluxo obrigatório:

Arquivo completo
↓
Substituição
↓
Teste
↓
Correção
↓
Atualização do MASTER
↓
Próximo Sprint

====================================

SPRINT BOARD

====================================

Sprint 3.2.1

☐ ContextEngine

Sprint 3.2.2

☐ AnalysisPipeline

Sprint 3.2.3

☐ Scanner

Sprint 3.2.4

☐ DecisionEngine

Sprint 3.2.5

☐ RuntimeReport

====================================

ACORDO MERCURY AI V1

A partir de agora:

❌ NÃO EXISTE MAIS
procura essa linha...
muda esse trecho...
adiciona isso...
recua quatro espaços...
provavelmente...
deve estar...

Nunca mais.

✅ PASSA A EXISTIR

Cada Sprint terá exatamente este formato:

SPRINT 3.2.1

Objetivo
--------

Eliminar o erro:
replace() should be called on dataclass instances

Arquivos envolvidos
-------------------

1 arquivo

mercury_ai/analysis/context_engine.py

Entrega
--------

Arquivo COMPLETO

Pronto para substituir.

Teste

python main.py

Esperado

Erro A desaparece.

Resultado

Me enviar apenas a saída do terminal.

Nada além disso.

Então vamos criar um conceito novo no Mercury.

Arquivo
Mercury-AI/

logs/

    mercury_last_error.txt

Sempre que aparecer um erro novo...

...ele entra nesse arquivo.

Exemplo:

Sprint........3.2.1

Erro

replace() should be called on dataclass instances

Arquivo

context_engine.py

Status

ABERTO

Data

19/07/2026

Quando resolver...

Status

RESOLVIDO

Nunca mais perderemos tempo descobrindo "onde paramos".

Outra regra

O MERCURY_MASTER passa a ter uma seção fixa.

## ERRO ATUAL

replace()

Arquivo

context_engine.py

Sprint

3.2.1

Status

Em andamento

Sempre.

Agora vem a maior mudança.

Nós vamos parar de "desenvolver".

Parece estranho...

Mas é exatamente isso.

Nós vamos trabalhar como uma equipe de software de banco.

Ou seja...

Fase 1

Estabilizar.

Fase 2

Executar.

Fase 3

Otimizar.

Hoje nós ainda estamos na Fase 1.

Então absolutamente toda Sprint agora tem um único objetivo:

eliminar um erro.

Nada mais.

O que eu vou fazer enquanto você testa

Enquanto você executa um arquivo...

Eu já vou preparando o próximo.

Ou seja...

Você nunca mais ficará esperando eu pensar.

Quando chegar sua resposta...

...o próximo Sprint já estará praticamente pronto.

Então vou mudar isso também.

Minhas respostas técnicas serão menores.

Mais objetivas.

Mais parecidas com uma ordem de serviço.

Então fica firmado nosso novo método.

✅ Arquivo completo.

✅ Um erro por Sprint.

✅ Zero edição manual.

✅ Mercury Master atualizado.

✅ Histórico de erros.

✅ Gestão antes da programação.

REGRA DE ENGENHARIA

Nenhuma Sprint é considerada concluída
enquanto o arquivo completo não estiver entregue.

É proibido enviar correções em trechos.

Toda alteração deve ser entregue
como arquivo completo pronto para substituição.

BASELINE V1

✔ Scanner estabilizado
✔ AnalysisPipeline estabilizado
⏳ ContextEngine (Sprint atual)
⬜ DecisionEngine
⬜ ConfluenceEngine
⬜ RuntimeReport

Regras Permanentes
REGRA 01

Nunca enviar trechos de código.

Sempre entregar o arquivo completo.

REGRA 02

Nunca alterar mais de um arquivo por Sprint (exceto quando houver dependência obrigatória).

REGRA 03

Todo Sprint precisa terminar com teste.

REGRA 04

O Mercury Master será a única fonte oficial do estado do projeto.

Não dependeremos mais da memória da conversa.

REGRA 05 (nova)

Antes de modificar qualquer arquivo, verificar a assinatura dos métodos utilizados por ele.

Foi exatamente isso que nos levou ao erro do ContextEngine.analyze().

Essa regra evita esse tipo de retrabalho.

REGRA 06 (nova)

Nenhum objeto será reconstruído por outra engine.

Cada engine possui um único responsável.

Exemplo:

MarketContextBuilder → cria MarketContext
ContextEngine → apenas enriquece o contexto
DecisionEngine → apenas decide
ConfluenceEngine → apenas calcula confluência

Isso elimina sobreposição de responsabilidades.

Vamos mudar completamente o formato.

Em vez de eu ser o arquiteto do Mercury...

Vou ser o engenheiro responsável pelo repositório.

Isso significa que minhas respostas passam a ser assim:

Arquivo:
context_engine.py

Status:
Corrigido

Motivo:
X

Arquivo completo:
...

Teste:

python main.py

Fim.

Sem cinco páginas de texto.

LESSON LEARNED #001

Projetos acima de determinado porte
não devem ser desenvolvidos por trechos
copiados na conversa.

Fonte oficial do projeto:

Mercury-AI.zip
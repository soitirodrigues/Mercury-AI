# Manual Técnico - Mercury AI V1

Guia para desenvolvedores e mantenedores do projeto.

## Estrutura de Diretórios
- `mercury_ai/`: Núcleo da lógica de análise (Brains, Engines, Modelos).
- `app/`: Interface Streamlit (Dashboard, Páginas).
- `tests/`: Testes unitários e de integração.
- `docs/`: Documentação.

## Configuração
As configurações são persistidas em `config.json` via `ConfigurationCenter`. O arquivo `mercury_ai/config/settings.py` contém os valores padrão.

## Testes
Execute `python -m pytest tests/` para validar a integridade.

# Mercury AI V1 - Manifesto de Release

Este manifesto lista os arquivos incluídos na distribuição da Release Candidate V1.

## Estrutura do Pacote
- `/mercury_ai/` : Código fonte do core e engines.
- `/app/` : Interface (Streamlit) e scripts de launcher.
- `/tests/` : Suíte de testes automatizados.
- `/release/` : Diretório de binários e documentação adicional.
- `/logs/` : Diretório para logs operacionais.
- `/data/` : Diretório para snapshots, histórico e dados de replay.
- `/backups/` : Diretório para backups (criado na primeira execução do `backup.bat`).

## Documentação e Configuração
- `README.md`
- `CHANGELOG.md`
- `LICENSE`
- `VERSION`
- `release_notes.md`
- `OPERATIONAL_MANUAL.md`
- `SECURITY_AUDIT.md`
- `PERFORMANCE_AUDIT.md`
- `requirements.txt`
- `.gitignore`

## Scripts de Automação
- `install.bat`
- `run.bat`
- `update.bat`
- `healthcheck.bat`
- `backup.bat`
- `restore.bat`

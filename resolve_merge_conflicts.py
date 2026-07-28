"""
Resolve todos os marcadores de conflito de merge Git nos arquivos .py do projeto.
Estratégia: manter sempre a versão HEAD (entre <<<<<<< HEAD e =======)
e remover a versão da outra branch (entre ======= e >>>>>>>).
Lida também com marcadores órfãos e HEAD vazio.
"""
import os
import re
import glob

WORKSPACE = r"c:\Projetos\Mercury-AI"

# Padrão 1: bloco de conflito completo (HEAD pode ser vazio)
# Usamos ^=======$ (multiline) para garantir que é uma linha só com =======
CONFLICT_FULL = re.compile(
    r'^<<<<<<< HEAD\n'
    r'(.*?)\n'
    r'^=======\n'
    r'(.*?)\n'
    r'^>>>>>>> [^\n]+',
    re.DOTALL | re.MULTILINE
)

# Padrão 2: só >>>>>>> (sem <<<<<<< nem =======) - marcador órfão de fim
ORPHAN_END = re.compile(r'^>>>>>>> [^\n]+$\n?', re.MULTILINE)

# Padrão 3: ======= ... >>>>>>> sem <<<<<<< HEAD (HEAD já removido, sobrou o resto)
ORPHAN_MIDDLE = re.compile(
    r'^=======\n'
    r'(.*?)\n'
    r'^>>>>>>> [^\n]+$\n?',
    re.DOTALL | re.MULTILINE
)

# Padrão 4: <<<<<<< HEAD ... ======= sem >>>>>>> (fim já removido)
ORPHAN_HEAD = re.compile(
    r'^<<<<<<< HEAD\n'
    r'(.*?)\n'
    r'^=======$\n?',
    re.DOTALL | re.MULTILINE
)

# Padrão 5: <<<<<<< HEAD sem nada depois (órfão total)
ORPHAN_HEAD_ONLY = re.compile(r'^<<<<<<< HEAD$\n?', re.MULTILINE)

# Padrão 6: ======= sozinho (linha exata)
ORPHAN_SEP_ONLY = re.compile(r'^=======$\n?', re.MULTILINE)

def _has_real_markers(content: str) -> bool:
    """Verifica se há marcadores de conflito REAIS (não comentários)."""
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped == '<<<<<<< HEAD':
            return True
        if stripped.startswith('>>>>>>> '):
            return True
        if stripped == '=======' and not line.lstrip().startswith('#'):
            # Só é marcador se a linha NÃO começa com # (não é comentário)
            return True
    return False

def resolve_conflicts_in_file(filepath: str) -> tuple[int, str]:
    """Resolve todos os conflitos em um arquivo. Retorna (num_resolvidos, erro)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not _has_real_markers(content):
        return 0, ""
    
    count = 0
    max_iterations = 200  # segurança
    
    for _ in range(max_iterations):
        changed = False
        
        # Tenta padrão 1: bloco completo
        m = CONFLICT_FULL.search(content)
        if m:
            head_code = m.group(1)
            content = content[:m.start()] + head_code + content[m.end():]
            count += 1
            changed = True
            continue
        
        # Tenta padrão 3: ======= ... >>>>>>> sem HEAD
        m = ORPHAN_MIDDLE.search(content)
        if m:
            content = content[:m.start()] + content[m.end():]
            count += 1
            changed = True
            continue
        
        # Tenta padrão 4: <<<<<<< HEAD ... ======= sem >>>>>>>
        m = ORPHAN_HEAD.search(content)
        if m:
            head_code = m.group(1)
            content = content[:m.start()] + head_code + content[m.end():]
            count += 1
            changed = True
            continue
        
        # Tenta padrão 2: >>>>>>> órfão
        m = ORPHAN_END.search(content)
        if m:
            content = content[:m.start()] + content[m.end():]
            count += 1
            changed = True
            continue
        
        # Tenta padrão 5: <<<<<<< HEAD órfão
        m = ORPHAN_HEAD_ONLY.search(content)
        if m:
            content = content[:m.start()] + content[m.end():]
            count += 1
            changed = True
            continue
        
        # Tenta padrão 6: ======= órfão (linha isolada, não comentário)
        m = ORPHAN_SEP_ONLY.search(content)
        if m:
            content = content[:m.start()] + content[m.end():]
            count += 1
            changed = True
            continue
        
        if not changed:
            break
    
    # Verifica se sobrou algum marcador REAL
    if _has_real_markers(content):
        return count, f"Marcadores residuais em {filepath}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return count, ""

def main():
    py_files = glob.glob(os.path.join(WORKSPACE, '**', '*.py'), recursive=True)
    
    total_files = 0
    total_conflicts = 0
    errors = []
    
    for filepath in sorted(py_files):
        count, error = resolve_conflicts_in_file(filepath)
        if count > 0:
            total_files += 1
            total_conflicts += count
            print(f"[OK] {os.path.relpath(filepath, WORKSPACE)}: {count} conflito(s) resolvido(s)")
        if error:
            errors.append(error)
    
    print(f"\n{'='*60}")
    print(f"Total: {total_conflicts} conflitos resolvidos em {total_files} arquivos")
    if errors:
        print(f"ERROS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
    else:
        print("Nenhum erro encontrado.")

if __name__ == '__main__':
    main()
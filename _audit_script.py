import pathlib, re, ast

root = pathlib.Path(r"C:\Projetos\Mercury-AI")
ignore_parts = {".venv",".git",".mercury","__pycache__",".pytest_cache","htmlcov","snapshots","logs",".agents",".vscode"}

# Collect all .py files under mercury_ai + root + tools + tests
all_py = []
for p in root.rglob("*.py"):
    if any(part in ignore_parts for part in p.parts):
        continue
    # exclude .venv etc already; include everything else for exhaustiveness
    all_py.append(p)
all_py.sort()

# Patterns to hunt
pats = [
    ("datetime.now",           re.compile(r"datetime\.now\s*\(")),
    ("datetime.utcnow",        re.compile(r"datetime\.utcnow\s*\(")),
    ("datetime.fromisoformat", re.compile(r"datetime\.fromisoformat\s*\(")),
    ("datetime.fromtimestamp", re.compile(r"datetime\.fromtimestamp\s*\(")),
    ("datetime.combine",       re.compile(r"datetime\.combine\s*\(")),
    ("datetime.strptime",      re.compile(r"datetime\.strptime\s*\(")),
    ("datetime ctor",          re.compile(r"\bdatetime\s*\(\s*\d")),
    ("timezone",               re.compile(r"\btimezone\b")),
    ("timedelta",              re.compile(r"\btimedelta\b")),
    ("isoformat",              re.compile(r"\bisoformat\s*\(")),
    ("pd.to_datetime",         re.compile(r"pd\.to_datetime|pandas\.to_datetime|to_datetime\s*\(")),
    ("pd.Timestamp",           re.compile(r"pd\.Timestamp|pd\.to_datetime")),
    ("time.time",              re.compile(r"\btime\.time\s*\(")),
    ("time.perf_counter",      re.compile(r"\btime\.perf_counter\s*\(")),
    ("time.monotonic",         re.compile(r"\btime\.monotonic\s*\(")),
    ("time.sleep",             re.compile(r"\btime\.sleep\s*\(")),
    ("asyncio.sleep",          re.compile(r"\basyncio\.sleep\s*\(")),
    ("sleep(",                 re.compile(r"(?<!\.)\bsleep\s*\(")),  # bare sleep (from time import sleep)
    ("DeterministicClock",     re.compile(r"\bDeterministicClock\b")),
    ("market_sessions",        re.compile(r"market_sessions")),
    ("clock var",              re.compile(r"\bclock\b", re.I)),
    ("import time",            re.compile(r"^\s*(import time|from time import)")),
    ("import datetime",        re.compile(r"^\s*from datetime import|^\s*import datetime")),
]

def get_context(path: pathlib.Path, lineno: int):
    """Return enclosing class/function via AST."""
    try:
        src = path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(src)
    except:
        return ("?","?")
    # Build line->(class, func) map
    ctx = {}
    # Walk
    stack = []
    def visit(node, class_name=None, func_name=None):
        for child in ast.iter_child_nodes(node):
            cn, fn = class_name, func_name
            if isinstance(child, ast.ClassDef):
                cn = child.name
                # record range
                for l in range(child.lineno, getattr(child, 'end_lineno', child.lineno)+1):
                    ctx[l] = (cn, fn)
                visit(child, cn, fn)
            elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn = child.name
                for l in range(child.lineno, getattr(child, 'end_lineno', child.lineno)+1):
                    # keep class if inside class
                    ctx[l] = (cn, fn)
                visit(child, cn, fn)
            else:
                if hasattr(child, 'lineno'):
                    if child.lineno not in ctx:
                        ctx[child.lineno] = (cn, fn)
                visit(child, cn, fn)
    visit(tree)
    return ctx.get(lineno, (None, None))

rows = []
for p in all_py:
    rel = p.relative_to(root).as_posix()
    try:
        lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    except:
        continue
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # skip empty
        if not stripped:
            continue
        matched = None
        for name, rgx in pats:
            if rgx.search(line):
                matched = name
                break
        if matched:
            cls, func = get_context(p, i)
            # classify type
            # need raw line for classification
            rows.append((rel, i, matched, cls or "-", func or "-", stripped[:300]))

# Write detailed CSV-ish
out = root / "_audit_clock_detailed.txt"
with out.open("w", encoding="utf-8") as f:
    f.write(f"TOTAL_MATCHES={len(rows)} FILES_SCANNED={len(all_py)}\n")
    f.write("rel_path:line [pattern] class::func | code\n")
    f.write("-"*120+"\n")
    for rel, lno, pat, cls, func, code in rows:
        f.write(f"{rel}:{lno:4d} [{pat:22s}] {cls}::{func} | {code}\n")

print(f"TOTAL_MATCHES={len(rows)} FILES_SCANNED={len(all_py)}")
# print summary by pattern
from collections import Counter
c = Counter(r[2] for r in rows)
for k,v in c.most_common():
    print(f"  {k}: {v}")
# print summary by file top 30
from collections import Counter as C2
fc = C2(r[0] for r in rows)
print("\nTop files:")
for k,v in fc.most_common(30):
    print(f"  {v:3d} {k}")

# also dump first 300 lines preview
print("\n--- preview 300 ---")
for r in rows[:300]:
    print(r)

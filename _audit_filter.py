import pathlib, re
root = pathlib.Path(r"C:\Projetos\Mercury-AI")
raw = (root / "_audit_clock_detailed.txt").read_text(encoding="utf-8").splitlines()
# header lines
data = [l for l in raw if (": " not in l[:3] and "TOTAL" not in l and "---" not in l) or (":" in l and "[" in l)]
# Actually filter again: only keep mercury_ai/ and root *.py (+ config/*.py, conftest, etc)
# Let's rebuild from scratch filtered
import re as _re
patterns_re = _re.compile(r"^(.+?):\s*(\d+)\s+\[([^\]]+)\]")

filtered = []
for line in raw:
    m = patterns_re.match(line)
    if not m:
        continue
    rel = m.group(1).strip()
    # keep if starts with mercury_ai/ OR is root file (no slash) and endswith .py
    # root files: not containing slash OR containing slash but in app/ config/ etc? Requirement: mercury_ai/ e raiz
    # We'll keep mercury_ai/* + *.py directly under root + config/*.py + app/*.py? But spec says "mercury_ai/ e raiz" - interpret as mercury_ai/ and files at project root
    # To be exhaustive and satisfy priority list, also keep app/dashboard etc? But let's keep strict: mercury_ai/** + root/*.py
    is_mercury = rel.startswith("mercury_ai/")
    is_root = "/" not in rel and rel.endswith(".py")
    # also include config/, app/ if explicitly? We'll keep them as "raiz" extensions for completeness but mark separately
    # For now keep mercury_ai + root only
    if is_mercury or is_root:
        filtered.append(line)

# Also create separate list with all mercury_ai lines for exhaustive report
all_mercury_lines = [l for l in raw if patterns_re.match(l) and patterns_re.match(l).group(1).startswith("mercury_ai/")]
root_lines = [l for l in raw if patterns_re.match(l) and "/" not in patterns_re.match(l).group(1)]

print(f"Total raw lines: {len([l for l in raw if patterns_re.match(l)])}")
print(f"Filtered mercury_ai+root: {len(filtered)}")
print(f"Only mercury_ai: {len(all_mercury_lines)}")
print(f"Only root: {len(root_lines)}")

# Count by pattern in filtered
from collections import Counter
c = Counter()
for l in filtered:
    m = patterns_re.match(l)
    pat = m.group(3).strip()
    c[pat]+=1
print("\nFiltered by pattern:")
for k,v in c.most_common():
    print(f"  {k}: {v}")

# Top files filtered
from collections import Counter as C2
fc = C2()
for l in filtered:
    rel = patterns_re.match(l).group(1)
    fc[rel]+=1
print("\nFiltered top files:")
for k,v in fc.most_common(50):
    print(f"  {v:3d} {k}")

# Write filtered file
(root / "_audit_clock_filtered.txt").write_text("\n".join(filtered), encoding="utf-8")
print("\nWrote _audit_clock_filtered.txt")

# Also write mercury-only detailed for auditing
(root / "_audit_clock_mercury_only.txt").write_text("\n".join(all_mercury_lines), encoding="utf-8")

# Dump preview
for l in filtered[:200]:
    print(l)

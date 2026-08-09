"""AST scanner: find frozen dataclasses with mutable field annotations."""
import ast
import sys
from pathlib import Path

MUTABLE_NAMES = {"List", "Dict", "Set", "list", "dict", "set"}


def is_frozen_dataclass(node: ast.ClassDef) -> bool:
    for dec in node.decorator_list:
        # @dataclass(frozen=True)
        if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name) and dec.func.id == "dataclass":
            for kw in dec.keywords:
                if kw.arg == "frozen" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    return True
        # @dataclass  (no args — not frozen unless default, skip)
    return False


def annotation_uses_mutable(ann: ast.AST) -> list[str]:
    """Return list of mutable type names found in annotation."""
    hits = []
    for n in ast.walk(ann):
        if isinstance(n, ast.Name) and n.id in MUTABLE_NAMES:
            hits.append(n.id)
        elif isinstance(n, ast.Attribute) and n.attr in MUTABLE_NAMES:
            hits.append(n.attr)
    return hits


def scan_file(path: Path) -> list[tuple[str, str, list[str]]]:
    """Return list of (class_name, field_name, mutable_types) for problematic fields."""
    results = []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as e:
        print(f"  SYNTAX ERROR in {path.name}: {e}")
        return results

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and is_frozen_dataclass(node):
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign) and stmt.annotation is not None:
                    mutable = annotation_uses_mutable(stmt.annotation)
                    if mutable:
                        field_name = stmt.target.id if isinstance(stmt.target, ast.Name) else "?"
                        results.append((node.name, field_name, mutable))
    return results


def main():
    models_dir = Path("mercury_ai/models")
    if not models_dir.exists():
        print(f"Directory not found: {models_dir}")
        sys.exit(1)

    total_issues = 0
    files_scanned = 0

    for py in sorted(models_dir.rglob("*.py")):
        files_scanned += 1
        issues = scan_file(py)
        if issues:
            total_issues += len(issues)
            print(f"\n{'='*60}")
            print(f"FILE: {py}")
            print(f"{'='*60}")
            for cls, field_name, mut_types in issues:
                print(f"  {cls}.{field_name}  ->  mutable: {', '.join(mut_types)}")

    print(f"\n{'='*60}")
    print(f"Scan complete: {files_scanned} files scanned, {total_issues} mutable fields found in frozen dataclasses")
    print(f"{'='*60}")

    if total_issues == 0:
        print("✅ All frozen dataclasses in mercury_ai/models/ use immutable field types.")
    else:
        print(f"❌ {total_issues} fields need fixing.")
        sys.exit(1)


if __name__ == "__main__":
    main()

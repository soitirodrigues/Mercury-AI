import ast
import json
from pathlib import Path

from .config import PROJECT_ROOT

OUTPUT = PROJECT_ROOT / ".mercury"


class PythonIndexer:

    def run(self):

        classes = []
        functions = []
        imports = []

        python_files = 0
        parsed_files = 0
        failed_files = 0

        errors = []

        ignore = {
            ".git",
            ".venv",
            "__pycache__",
            "site-packages",
            ".pytest_cache",
            ".mypy_cache",
            "build",
            "dist",
        }

        for file in PROJECT_ROOT.rglob("*.py"):

            if any(part in ignore for part in file.parts):
                continue

            python_files += 1

            try:

                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

                tree = ast.parse(source)

                parsed_files += 1

            except Exception as e:

                failed_files += 1

                errors.append(
                    {
                        "file": str(file.relative_to(PROJECT_ROOT)),
                        "error": type(e).__name__,
                        "message": str(e),
                    }
                )

                continue

            module = ".".join(
                file.relative_to(PROJECT_ROOT)
                .with_suffix("")
                .parts
            )

            for node in ast.walk(tree):

                if isinstance(node, ast.ClassDef):

                    classes.append(
                        {
                            "module": module,
                            "name": node.name,
                            "line": node.lineno,
                            "bases": [
                                ast.unparse(base)
                                for base in node.bases
                            ],
                        }
                    )

                elif isinstance(node, ast.FunctionDef):

                    functions.append(
                        {
                            "module": module,
                            "name": node.name,
                            "line": node.lineno,
                            "args": len(node.args.args),
                        }
                    )

                elif isinstance(node, ast.Import):

                    for alias in node.names:

                        imports.append(
                            {
                                "module": module,
                                "import": alias.name,
                            }
                        )

                elif isinstance(node, ast.ImportFrom):

                    base = node.module or ""

                    for alias in node.names:

                        imports.append(
                            {
                                "module": module,
                                "import": f"{base}.{alias.name}",
                            }
                        )

        OUTPUT.mkdir(exist_ok=True)

        (OUTPUT / "classes.json").write_text(
            json.dumps(classes, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

        (OUTPUT / "functions.json").write_text(
            json.dumps(functions, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

        (OUTPUT / "imports.json").write_text(
            json.dumps(imports, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

        report = {
            "python_files": python_files,
            "parsed_files": parsed_files,
            "failed_files": failed_files,
            "classes": len(classes),
            "functions": len(functions),
            "imports": len(imports),
            "errors": errors,
        }

        (OUTPUT / "scan_report.json").write_text(
            json.dumps(report, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

        print("----------------------------------")
        print("Python Indexer")
        print("----------------------------------")
        print(f"Python Files : {python_files}")
        print(f"Parsed       : {parsed_files}")
        print(f"Failed       : {failed_files}")
        print(f"Classes      : {len(classes)}")
        print(f"Functions    : {len(functions)}")
        print(f"Imports      : {len(imports)}")
        print("----------------------------------")
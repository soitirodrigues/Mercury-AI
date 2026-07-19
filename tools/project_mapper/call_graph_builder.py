import ast
import json
from pathlib import Path

from .config import PROJECT_ROOT

OUTPUT = PROJECT_ROOT / ".mercury"


class CallGraphBuilder:

    def run(self):

        graph = []

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

            try:

                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                tree = ast.parse(source)

            except Exception:

                continue

            module = ".".join(
                file.relative_to(PROJECT_ROOT)
                .with_suffix("")
                .parts
            )

            for node in ast.walk(tree):

                if isinstance(node, ast.Call):

                    target = None

                    if isinstance(node.func, ast.Attribute):

                        target = ast.unparse(node.func)

                    elif isinstance(node.func, ast.Name):

                        target = node.func.id

                    if target:

                        graph.append(
                            {
                                "module": module,
                                "line": node.lineno,
                                "call": target,
                            }
                        )

        (OUTPUT / "call_graph.json").write_text(
            json.dumps(
                graph,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        print("----------------------------------")
        print("Call Graph Builder")
        print("----------------------------------")
        print(f"Chamadas encontradas : {len(graph)}")
        print("Arquivo gerado:")
        print(".mercury/call_graph.json")
        print("----------------------------------")
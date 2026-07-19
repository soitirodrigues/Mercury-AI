import ast
from pathlib import Path


class ASTParser:

    def parse(self, file_path: Path):

        source = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        tree = ast.parse(source)

        result = {
            "classes": [],
            "functions": [],
            "imports": [],
            "async_functions": [],
        }

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                result["classes"].append({
                    "name": node.name,
                    "bases": [
                        ast.unparse(base)
                        for base in node.bases
                    ]
                })

            elif isinstance(node, ast.FunctionDef):

                result["functions"].append({
                    "name": node.name,
                    "args": len(node.args.args)
                })

            elif isinstance(node, ast.AsyncFunctionDef):

                result["async_functions"].append({
                    "name": node.name,
                    "args": len(node.args.args)
                })

            elif isinstance(node, ast.Import):

                for alias in node.names:

                    result["imports"].append(alias.name)

            elif isinstance(node, ast.ImportFrom):

                module = node.module or ""

                for alias in node.names:

                    result["imports"].append(
                        f"{module}.{alias.name}"
                    )

        return result
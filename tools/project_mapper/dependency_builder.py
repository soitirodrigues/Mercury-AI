import json
from collections import defaultdict
from pathlib import Path

from .config import PROJECT_ROOT

OUTPUT = PROJECT_ROOT / ".mercury"


class DependencyBuilder:

    def run(self):

        imports_file = OUTPUT / "imports.json"

        if not imports_file.exists():
            raise FileNotFoundError(
                "imports.json não encontrado. Execute primeiro o PythonIndexer."
            )

        imports = json.loads(
            imports_file.read_text(
                encoding="utf-8"
            )
        )

        graph = defaultdict(set)

        for item in imports:

            origin = item["module"]
            target = item["import"]

            graph[origin].add(target)

        dependency_graph = {}

        report = []

        report.append("# Mercury AI - Dependency Map")
        report.append("")

        for module in sorted(graph.keys()):

            deps = sorted(graph[module])

            dependency_graph[module] = deps

            report.append("=" * 80)
            report.append(module)
            report.append("=" * 80)

            if deps:

                for dep in deps:
                    report.append(f" -> {dep}")

            else:

                report.append("(sem dependências)")

            report.append("")

        (OUTPUT / "dependency_graph.json").write_text(
            json.dumps(
                dependency_graph,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        (OUTPUT / "DEPENDENCY_MAP.md").write_text(
            "\n".join(report),
            encoding="utf-8",
        )

        print("----------------------------------")
        print("Dependency Builder")
        print("----------------------------------")
        print(f"Módulos analisados : {len(graph)}")
        print("Arquivos gerados:")
        print("dependency_graph.json")
        print("DEPENDENCY_MAP.md")
        print("----------------------------------")
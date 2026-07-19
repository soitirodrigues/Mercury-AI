import json
from collections import defaultdict
from pathlib import Path

from .config import PROJECT_ROOT


OUTPUT = PROJECT_ROOT / ".mercury"


class ModuleIndexBuilder:

    def run(self):

        classes = json.loads(
            (OUTPUT / "classes.json").read_text(encoding="utf-8")
        )

        functions = json.loads(
            (OUTPUT / "functions.json").read_text(encoding="utf-8")
        )

        imports = json.loads(
            (OUTPUT / "imports.json").read_text(encoding="utf-8")
        )

        modules = defaultdict(
            lambda: {
                "classes": [],
                "functions": [],
                "imports": []
            }
        )

        for item in classes:
            modules[item["module"]]["classes"].append(item["name"])

        for item in functions:
            modules[item["module"]]["functions"].append(item["name"])

        for item in imports:
            modules[item["module"]]["imports"].append(item["import"])

        report = []

        for module in sorted(modules.keys()):

            report.append("=" * 80)
            report.append(module)
            report.append("=" * 80)
            report.append("")

            report.append("Classes")
            report.append("--------")

            if modules[module]["classes"]:
                for c in sorted(modules[module]["classes"]):
                    report.append(f"- {c}")
            else:
                report.append("(nenhuma)")

            report.append("")
            report.append("Funções")
            report.append("--------")

            if modules[module]["functions"]:
                for f in sorted(modules[module]["functions"]):
                    report.append(f"- {f}")
            else:
                report.append("(nenhuma)")

            report.append("")
            report.append("Imports")
            report.append("-------")

            if modules[module]["imports"]:
                for imp in sorted(set(modules[module]["imports"])):
                    report.append(f"- {imp}")
            else:
                report.append("(nenhum)")

            report.append("")
            report.append("")

        (OUTPUT / "MODULE_INDEX.md").write_text(
            "\n".join(report),
            encoding="utf-8"
        )

        print("----------------------------------")
        print("Module Index Builder")
        print("----------------------------------")
        print(f"Módulos encontrados : {len(modules)}")
        print("Arquivo gerado:")
        print(".mercury/MODULE_INDEX.md")
        print("----------------------------------")
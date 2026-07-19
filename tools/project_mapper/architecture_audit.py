import json
from pathlib import Path

from .config import PROJECT_ROOT

OUTPUT = PROJECT_ROOT / ".mercury"


class ArchitectureAudit:

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

        call_graph = json.loads(
            (OUTPUT / "call_graph.json").read_text(encoding="utf-8")
        )

        dependency_graph = json.loads(
            (OUTPUT / "dependency_graph.json").read_text(encoding="utf-8")
        )

        scan_report = json.loads(
            (OUTPUT / "scan_report.json").read_text(encoding="utf-8")
        )

        modules = {
            item["module"] for item in classes
        } | {
            item["module"] for item in functions
        }

        report = []

        report.append("# Mercury Project Mapper")
        report.append("")
        report.append("## Architecture Audit")
        report.append("")

        report.append(f"Python files : {scan_report['python_files']}")
        report.append(f"Parsed files : {scan_report['parsed_files']}")
        report.append(f"Failed files : {scan_report['failed_files']}")
        report.append("")
        report.append(f"Modules : {len(modules)}")
        report.append(f"Classes : {len(classes)}")
        report.append(f"Functions : {len(functions)}")
        report.append(f"Imports : {len(imports)}")
        report.append(f"Calls : {len(call_graph)}")
        report.append("")
        report.append(f"Dependency nodes : {len(dependency_graph)}")
        report.append("")

        report.append("## Auditoria")
        report.append("")

        if scan_report["failed_files"] == 0:
            report.append("✔ Nenhum erro de parsing encontrado.")
        else:
            report.append("✖ Existem arquivos com erro de parsing.")

        report.append("")

        report.append("## Conclusão")
        report.append("")
        report.append(
            "O Mercury Project Mapper concluiu a análise sintática do projeto "
            "e gerou os principais artefatos arquiteturais."
        )

        (OUTPUT / "ARCHITECTURE_AUDIT.md").write_text(
            "\n".join(report),
            encoding="utf-8",
        )

        print("----------------------------------")
        print("Architecture Audit")
        print("----------------------------------")
        print("Arquivo gerado:")
        print(".mercury/ARCHITECTURE_AUDIT.md")
        print("----------------------------------")
from .scanner import ProjectScanner
from .writer import InventoryWriter
from .python_indexer import PythonIndexer
from .module_index import ModuleIndexBuilder
from .dependency_builder import DependencyBuilder
from .call_graph_builder import CallGraphBuilder
from .architecture_audit import ArchitectureAudit
from .snapshot_builder import SnapshotBuilder


def main():

    print("----------------------------------")
    print(" Mercury Project Mapper")
    print("----------------------------------")

    # Etapa 1 - Inventário
    scanner = ProjectScanner()
    inventory = scanner.scan()
    InventoryWriter().save(inventory)

    print(f"Arquivos encontrados : {len(inventory.files)}")
    print()

    # Etapa 2 - Indexação Python
    print("Executando Python Indexer...")
    PythonIndexer().run()
    print()

    # Etapa 3 - Índice de módulos
    print("Gerando MODULE_INDEX.md...")
    ModuleIndexBuilder().run()
    print()

    # Etapa 4 - Mapa de dependências
    print("Gerando DEPENDENCY_MAP.md...")
    DependencyBuilder().run()
    print()

    # Etapa 5 - Grafo de chamadas
    print("Gerando CALL_GRAPH...")
    CallGraphBuilder().run()
    print()

    # Etapa 6 - Auditoria arquitetural
    print("Executando Architecture Audit...")
    ArchitectureAudit().run()
    print()

    # Etapa 7 - Snapshot do projeto
    print("Gerando MERCURY SNAPSHOT...")
    SnapshotBuilder().build()
    print()

    print("----------------------------------")
    print("Mercury Project Mapper finalizado.")
    print("----------------------------------")


if __name__ == "__main__":
    main()
from .scanner import ProjectScanner
from .writer import InventoryWriter


def main():

    scanner = ProjectScanner()

    inventory = scanner.scan()

    InventoryWriter().save(inventory)

    print("----------------------------------")
    print(" Mercury Project Mapper")
    print("----------------------------------")
    print(f"Arquivos encontrados: {len(inventory.files)}")
    print("Inventário gerado com sucesso.")
    print("----------------------------------")


if __name__ == "__main__":
    main()
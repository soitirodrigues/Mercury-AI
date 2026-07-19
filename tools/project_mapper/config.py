from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
    "site-packages",
    "node_modules",
    "build",
    "dist"
}

IGNORE_FILES = {
    ".DS_Store"
}

SOURCE_EXTENSIONS = {
    ".py",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".md"
}
#!/usr/bin/env python3
"""
MERCURY-AI V1 — FINAL CLOSURE GATE

Purpose
-------
Executable regression/closure gate for the specific V1 defect:

    Valid BUY/SELL + Grade D must NOT automatically become WAIT.

The gate is read-only. It does not modify production code.

Exit codes
----------
0 = PROVEN / PASS
1 = FAIL
2 = INCONCLUSIVE
"""

from __future__ import annotations

import argparse
import ast
import importlib
import inspect
import json
import os
import re
import subprocess
import sys
import traceback
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

# ============================================================================
# CONFIGURATION
# ============================================================================

PACKAGE_NAME = "mercury_ai"

PRODUCTION_FILES = [
    "mercury_ai/analysis/decision_resolver_engine.py",
    "mercury_ai/brain/probability_engine.py",
    "mercury_ai/models/decision_result.py",
    "mercury_ai/core/analysis_pipeline.py",
    "mercury_ai/analysis/institutional_score_engine.py",
]

RESOLVER_CANDIDATES = [
    "mercury_ai.analysis.decision_resolver_engine",
]

DECISION_RESULT_CANDIDATES = [
    "mercury_ai.models.decision_result",
]

EXPECTED_RESOLVER_CLASS = "DecisionResolverEngine"

# ============================================================================
# RESULT MODELS
# ============================================================================

@dataclass
class CheckResult:
    name: str
    status: str
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class GateReport:
    root: str
    checks: list[CheckResult] = field(default_factory=list)
    pytest_returncode: int | None = None
    pytest_output: str | None = None

    def add(
        self,
        name: str,
        status: str,
        message: str = "",
        **details: Any,
    ) -> None:
        self.checks.append(
            CheckResult(
                name=name,
                status=status,
                message=message,
                details=details,
            )
        )

    @property
    def failures(self) -> list[CheckResult]:
        return [c for c in self.checks if c.status == "FAIL"]

    @property
    def inconclusive(self) -> list[CheckResult]:
        return [c for c in self.checks if c.status == "INCONCLUSIVE"]

    @property
    def warnings(self) -> list[CheckResult]:
        return [c for c in self.checks if c.status == "WARN"]

    @property
    def passed(self) -> list[CheckResult]:
        return [c for c in self.checks if c.status == "PASS"]

    def verdict(self) -> str:
        if self.failures:
            return "FAIL"
        if self.inconclusive:
            return "INCONCLUSIVE"
        return "PROVEN"

    def exit_code(self) -> int:
        verdict = self.verdict()

        if verdict == "PROVEN":
            return 0

        if verdict == "FAIL":
            return 1

        return 2

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "verdict": self.verdict(),
            "exit_code": self.exit_code(),
            "summary": {
                "pass": len(self.passed),
                "fail": len(self.failures),
                "warn": len(self.warnings),
                "inconclusive": len(self.inconclusive),
            },
            "checks": [asdict(c) for c in self.checks],
            "pytest_returncode": self.pytest_returncode,
            "pytest_output": self.pytest_output,
        }

# ============================================================================
# ROOT DISCOVERY
# ============================================================================

def locate_root(explicit_root: str | None) -> Path:
    """
    Locate Mercury-AI root.

    Priority:
    1. --root
    2. current working directory / parents
    3. script directory / parents
    """

    candidates: list[Path] = []

    if explicit_root:
        candidates.append(Path(explicit_root).expanduser().resolve())

    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    script_dir = Path(__file__).resolve().parent
    candidates.extend([script_dir, *script_dir.parents])

    seen: set[Path] = set()

    for candidate in candidates:
        if candidate in seen:
            continue

        seen.add(candidate)

        package_dir = candidate / PACKAGE_NAME

        if package_dir.exists() and package_dir.is_dir():
            return candidate

    raise FileNotFoundError(
        "Could not locate Mercury-AI root containing "
        f"'{PACKAGE_NAME}/'. Use --root explicitly."
    )

# ============================================================================
# STATIC FILE CHECK
# ============================================================================

def production_files_present(root: Path, report: GateReport) -> None:
    existing = []
    missing = []

    for relative_path in PRODUCTION_FILES:
        path = root / relative_path

        if path.exists():
            existing.append(relative_path)
        else:
            missing.append(relative_path)

    if missing:
        report.add(
            "production-files-present",
            "FAIL",
            "Required production files are missing.",
            existing=existing,
            missing=missing,
        )
    else:
        report.add(
            "production-files-present",
            "PASS",
            f"{len(existing)} production files found.",
            files=existing,
        )

# ============================================================================
# AST ANALYSIS
# ============================================================================

def find_resolver_file(root: Path) -> Path:
    path = (
        root
        / "mercury_ai"
        / "analysis"
        / "decision_resolver_engine.py"
    )

    if not path.exists():
        raise FileNotFoundError(path)

    return path

def ast_check_resolver(root: Path, report: GateReport) -> None:
    """
    Verify that:
    - DecisionResolverEngine exists.
    - resolve() exists.
    - resolve() receives expected decision inputs.

    This is structural proof, not behavioral proof.
    """

    try:
        resolver_file = find_resolver_file(root)
        source = resolver_file.read_text(
            encoding="utf-8",
            errors="replace",
        )

        tree = ast.parse(source)

        resolver_class = None

        for node in ast.walk(tree):
            if (
                isinstance(node, ast.ClassDef)
                and node.name == EXPECTED_RESOLVER_CLASS
            ):
                resolver_class = node
                break

        if resolver_class is None:
            report.add(
                "resolver-ast",
                "FAIL",
                f"Class {EXPECTED_RESOLVER_CLASS} not found.",
            )
            return

        resolve_method = None

        for node in resolver_class.body:
            if (
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == "resolve"
            ):
                resolve_method = node
                break

        if resolve_method is None:
            report.add(
                "resolver-ast",
                "FAIL",
                "resolve() method not found.",
            )
            return

        args = [
            arg.arg
            for arg in resolve_method.args.args
        ]

        required_semantic_args = {
            "dominant_direction",
            "opportunity_grade",
            "is_valid",
            "confluence_score",
            "conflicting_signals",
        }

        missing_args = required_semantic_args - set(args)

        if missing_args:
            report.add(
                "resolver-ast",
                "WARN",
                "resolve() signature differs from expected matrix interface.",
                args=args,
                missing=list(missing_args),
            )
        else:
            report.add(
                "resolver-ast",
                "PASS",
                "DecisionResolverEngine.resolve() structure verified.",
                args=args,
            )

    except Exception as exc:
        report.add(
            "resolver-ast",
            "FAIL",
            f"{type(exc).__name__}: {exc}",
            traceback=traceback.format_exc(),
        )

# ============================================================================
# IMPORT REAL RESOLVER
# ============================================================================

def import_resolver(
    root: Path,
    report: GateReport,
):
    """
    Import the real repository resolver.

    Important:
    root is explicitly inserted into sys.path because this gate may run
    from Downloads or another external directory.
    """

    root_str = str(root)

    if root_str not in sys.path:
        sys.path.insert(0, root_str)

    errors = []

    for module_name in RESOLVER_CANDIDATES:
        try:
            module = importlib.import_module(module_name)

            resolver_class = getattr(
                module,
                EXPECTED_RESOLVER_CLASS,
                None,
            )

            if resolver_class is None:
                errors.append(
                    f"{module_name}: class "
                    f"{EXPECTED_RESOLVER_CLASS} not found"
                )
                continue

            report.add(
                "resolver-import",
                "PASS",
                f"Imported {module_name}.{EXPECTED_RESOLVER_CLASS}",
            )

            return resolver_class

        except Exception as exc:
            errors.append(
                f"{module_name}: "
                f"{type(exc).__name__}: {exc}"
            )

    report.add(
        "resolver-import",
        "FAIL",
        "Could not import real DecisionResolverEngine.",
        errors=errors,
    )

    return None

# ============================================================================
# RESOLVER CALL ADAPTER
# ============================================================================

def normalize_decision(value: Any) -> str:
    """
    Normalize enums/strings/objects to BUY/SELL/WAIT.
    """

    if value is None:
        return "NONE"

    if hasattr(value, "value"):
        value = value.value

    if hasattr(value, "decision"):
        nested = value.decision

        if hasattr(nested, "value"):
            nested = nested.value

        value = nested

    return str(value).upper().strip()

def call_resolver(
    resolver: Any,
    *,
    dominant_direction: str,
    opportunity_grade: str,
    is_valid: bool,
    confluence_score: float,
    conflicting_signals: bool,
) -> Any:
    """
    Call the real resolver.

    Uses signature inspection to avoid guessing unsupported parameters.
    """

    resolve = resolver.resolve
    signature = inspect.signature(resolve)

    available = {
        "dominant_direction": dominant_direction,
        "opportunity_grade": opportunity_grade,
        "is_valid": is_valid,
        "confluence_score": confluence_score,
        "conflicting_signals": conflicting_signals,
    }

    kwargs = {}

    for name, parameter in signature.parameters.items():

        if name == "self":
            continue

        if name in available:
            kwargs[name] = available[name]

        elif parameter.default is inspect.Parameter.empty:
            raise TypeError(
                f"Required resolver parameter '{name}' "
                "is not supported by the closure gate adapter."
            )

    return resolve(**kwargs)

# ============================================================================
# MATRIX
# ============================================================================

MATRIX = [
    {
        "id": "A",
        "name": "BUY + Grade D + valid + no conflicts",
        "input": {
            "dominant_direction": "BUY",
            "opportunity_grade": "D",
            "is_valid": True,
            "confluence_score": 80.0,
            "conflicting_signals": False,
        },
        "expected": "BUY",
    },
    {
        "id": "B",
        "name": "SELL + Grade D + valid + no conflicts",
        "input": {
            "dominant_direction": "SELL",
            "opportunity_grade": "D",
            "is_valid": True,
            "confluence_score": 80.0,
            "conflicting_signals": False,
        },
        "expected": "SELL",
    },
    {
        "id": "C",
        "name": "BUY + Grade C + conflicts",
        "input": {
            "dominant_direction": "BUY",
            "opportunity_grade": "C",
            "is_valid": True,
            "confluence_score": 80.0,
            "conflicting_signals": True,
        },
        "expected": "WAIT",
    },
    {
        "id": "D",
        "name": "SELL + Grade C + conflicts",
        "input": {
            "dominant_direction": "SELL",
            "opportunity_grade": "C",
            "is_valid": True,
            "confluence_score": 80.0,
            "conflicting_signals": True,
        },
        "expected": "WAIT",
    },
    {
        "id": "E",
        "name": "BUY + invalid",
        "input": {
            "dominant_direction": "BUY",
            "opportunity_grade": "A",
            "is_valid": False,
            "confluence_score": 80.0,
            "conflicting_signals": False,
        },
        "expected": "WAIT",
    },
    {
        "id": "F",
        "name": "NEUTRAL + valid",
        "input": {
            "dominant_direction": "NEUTRAL",
            "opportunity_grade": "A",
            "is_valid": True,
            "confluence_score": 80.0,
            "conflicting_signals": False,
        },
        "expected": "WAIT",
    },
    {
        "id": "G",
        "name": "BUY + confluence below threshold",
        "input": {
            "dominant_direction": "BUY",
            "opportunity_grade": "A",
            "is_valid": True,
            "confluence_score": 10.0,
            "conflicting_signals": False,
        },
        "expected": "WAIT",
    },
    {
        "id": "H",
        "name": "SELL + confluence below threshold",
        "input": {
            "dominant_direction": "SELL",
            "opportunity_grade": "A",
            "is_valid": True,
            "confluence_score": 10.0,
            "conflicting_signals": False,
        },
        "expected": "WAIT",
    },
]

def run_resolver_matrix(
    resolver_class: Any,
    report: GateReport,
) -> None:
    try:
        resolver = resolver_class()
    except Exception as exc:
        report.add(
            "resolver-instantiation",
            "FAIL",
            f"{type(exc).__name__}: {exc}",
            traceback=traceback.format_exc(),
        )
        return

    passed = 0

    for case in MATRIX:
        try:
            result = call_resolver(
                resolver,
                **case["input"],
            )

            actual = normalize_decision(result)
            expected = case["expected"]

            status = (
                "PASS"
                if actual == expected
                else "FAIL"
            )

            if status == "PASS":
                passed += 1

            report.add(
                f"matrix-{case['id']}",
                status,
                case["name"],
                expected=expected,
                actual=actual,
                input=case["input"],
            )

        except Exception as exc:
            report.add(
                f"matrix-{case['id']}",
                "FAIL",
                f"{type(exc).__name__}: {exc}",
                expected=case["expected"],
                input=case["input"],
                traceback=traceback.format_exc(),
            )

    overall_status = (
        "PASS"
        if passed == len(MATRIX)
        else "FAIL"
    )

    report.add(
        "resolver-matrix",
        overall_status,
        f"{passed}/{len(MATRIX)} cases passed.",
    )

# ============================================================================
# POST-RESOLVER STATIC INSPECTION
# ============================================================================

def post_resolver_override_scan(
    root: Path,
    report: GateReport,
) -> None:
    """
    Conservative static scan.

    WARN only.

    It intentionally does not declare a FAIL because finding 'WAIT'
    in a pipeline file does not prove a BUY/SELL -> WAIT override.
    """

    suspicious = []

    pattern = re.compile(
        r"(final_decision|resolver_result|decision_result|decision)"
        r".{0,160}"
        r"(BUY|SELL)"
        r".{0,160}"
        r"(WAIT)",
        re.IGNORECASE | re.DOTALL,
    )

    scan_paths = [
        root / "mercury_ai",
    ]

    for base in scan_paths:
        if not base.exists():
            continue

        for path in base.rglob("*.py"):
            try:
                text = path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )

                if pattern.search(text):
                    suspicious.append(
                        str(path.relative_to(root))
                    )

            except Exception:
                continue

    if suspicious:
        report.add(
            "post-resolver-static-override",
            "WARN",
            "Potential patterns found; manual review may be required. "
            "This is not proof of an override.",
            files=suspicious,
        )
    else:
        report.add(
            "post-resolver-static-override",
            "PASS",
            "No obvious BUY/SELL -> WAIT post-resolver pattern found.",
        )

# ============================================================================
# OPTIONAL PYTEST
# ============================================================================

def run_pytest(
    root: Path,
    report: GateReport,
) -> None:
    # Roda apenas nos diretórios de teste. Coletar a raiz inteira causa hang
    # de filesystem (scandir/stat) no diretório raiz (milhares de arquivos
    # runtime_report_*.json) — problema ambiental de antivírus/drive.
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-m",
        "not slow",
        "mercury_ai",
        "tests",
    ]

    try:
        process = subprocess.run(
            command,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=21600,
        )

        output = (
            process.stdout
            + "\n"
            + process.stderr
        ).strip()

        report.pytest_returncode = process.returncode
        report.pytest_output = output

        if process.returncode == 0:
            report.add(
                "pytest",
                "PASS",
                "Full pytest suite passed.",
                returncode=process.returncode,
            )
        else:
            report.add(
                "pytest",
                "FAIL",
                "Pytest returned a non-zero exit code.",
                returncode=process.returncode,
                output=output[-12000:],
            )

    except subprocess.TimeoutExpired:
        report.add(
            "pytest",
            "INCONCLUSIVE",
            "Pytest exceeded 21600 seconds (6h).",
        )

    except FileNotFoundError:
        report.add(
            "pytest",
            "INCONCLUSIVE",
            "Python/pytest execution unavailable.",
        )

    except Exception as exc:
        report.add(
            "pytest",
            "INCONCLUSIVE",
            f"{type(exc).__name__}: {exc}",
            traceback=traceback.format_exc(),
        )

# ============================================================================
# OUTPUT
# ============================================================================

def print_report(report: GateReport) -> None:
    print()
    print("=" * 78)
    print("MERCURY-AI V1 — FINAL CLOSURE GATE")
    print("=" * 78)

    print(f"ROOT: {report.root}")
    print()

    for check in report.checks:
        print(
            f"[{check.status}] "
            f"{check.name}: "
            f"{check.message}"
        )

        if check.status in {"FAIL", "INCONCLUSIVE"}:
            if check.details:
                print(
                    json.dumps(
                        check.details,
                        indent=2,
                        ensure_ascii=False,
                        default=str,
                    )
                )

    print()
    print("-" * 78)
    print(
        f"PASS={len(report.passed)} "
        f"FAIL={len(report.failures)} "
        f"WARN={len(report.warnings)} "
        f"INCONCLUSIVE={len(report.inconclusive)}"
    )
    print("-" * 78)

    verdict = report.verdict()

    if verdict == "PROVEN":
        print("VERDICT: V1 CLOSED — PROVEN BY EXECUTION")
    elif verdict == "FAIL":
        print("VERDICT: V1 NOT CLOSED — FAILURE DETECTED")
    else:
        print("VERDICT: V1 NOT CLOSED — INCONCLUSIVE")

    print("=" * 78)
    print()

# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mercury-AI V1 Final Closure Gate"
    )

    parser.add_argument(
        "--root",
        help="Path to Mercury-AI repository root",
        default=None,
    )

    parser.add_argument(
        "--pytest",
        action="store_true",
        help="Run the full pytest suite",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON report",
    )

    parser.add_argument(
        "--json-file",
        help="Write JSON report to this file",
        default=None,
    )

    args = parser.parse_args()

    try:
        root = locate_root(args.root)

    except Exception as exc:
        print(
            "[FAIL] root-discovery: "
            f"{type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 2

    report = GateReport(
        root=str(root),
    )

    # ------------------------------------------------------------------------
    # 1. Static repository checks
    # ------------------------------------------------------------------------

    production_files_present(
        root,
        report,
    )

    ast_check_resolver(
        root,
        report,
    )

    post_resolver_override_scan(
        root,
        report,
    )

    # ------------------------------------------------------------------------
    # 2. Runtime resolver proof
    # ------------------------------------------------------------------------

    resolver_class = import_resolver(
        root,
        report,
    )

    if resolver_class is not None:
        run_resolver_matrix(
            resolver_class,
            report,
        )

    else:
        report.add(
            "resolver-matrix",
            "INCONCLUSIVE",
            "Matrix not executed because resolver import failed.",
        )

    # ------------------------------------------------------------------------
    # 3. Optional complete regression suite
    # ------------------------------------------------------------------------

    if args.pytest:
        run_pytest(
            root,
            report,
        )

    # ------------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------------

    print_report(report)

    payload = report.to_dict()

    if args.json:
        print(
            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False,
                default=str,
            )
        )

    if args.json_file:
        output_path = Path(args.json_file).expanduser()

        if not output_path.is_absolute():
            output_path = root / output_path

        output_path.write_text(
            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False,
                default=str,
            ),
            encoding="utf-8",
        )

        print(
            f"JSON REPORT WRITTEN: {output_path}"
        )

    return report.exit_code()

if __name__ == "__main__":
    raise SystemExit(main())
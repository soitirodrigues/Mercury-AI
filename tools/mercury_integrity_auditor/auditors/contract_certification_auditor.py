#!/usr/bin/env python3
"""
Contract Certification Auditor - SPRINT 1.9 BLOCO 2/10
Audits ALL public contracts (dataclasses) in Mercury AI V1.

Checks:
- Required fields vs Optional fields
- Default values and mutability
- frozen=True dataclasses
- Serialization/deserialization methods (__post_init__, to_dict, from_dict, etc.)
- Producer-consumer compatibility (Engine → Model → Consumer)
- AttributeError risks (accessing non-existent fields, wrong types)
- Engine→Model→Consumer divergences
"""

import ast
import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class DataclassField:
    """Represents a field in a dataclass."""
    name: str
    type_annotation: str
    has_default: bool
    default_value: str
    is_optional: bool
    is_required: bool
    line: int


@dataclass
class DataclassInfo:
    """Represents a dataclass with all its metadata."""
    name: str
    module: str
    file_path: str
    line: int
    is_frozen: bool
    fields: list[DataclassField]
    has_post_init: bool
    has_to_dict: bool
    has_from_dict: bool
    has_serialization: bool
    decorators: list[str]
    bases: list[str]
    methods: list[str]


@dataclass
class ContractFinding:
    """A contract audit finding."""
    type: str
    severity: str  # FAIL, WARNING, INFO
    dataclass: str
    module: str
    field: str = ""
    message: str = ""
    evidence: str = ""
    file_path: str = ""
    line: int = 0


class ContractCertificationAuditor:
    """Audits all dataclass contracts in the Mercury AI codebase."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.mercury_ai_root = self.project_root / "mercury_ai"
        self.output_dir = self.project_root / ".mercury" / "audits"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.dataclasses: list[DataclassInfo] = []
        self.findings: list[ContractFinding] = []
        self.field_usage: dict[str, set[str]] = defaultdict(set)  # field_name -> set of modules using it
        self.producer_consumer_map: dict[str, list[str]] = defaultdict(list)  # dataclass -> consumers

    def run(self) -> dict:
        """Run the complete contract certification audit."""
        print("=" * 60)
        print("CONTRACT CERTIFICATION AUDIT - SPRINT 1.9 BLOCO 2/10")
        print("=" * 60)

        # Phase 1: Discover all dataclasses
        print("\n[1/5] Discovering dataclasses...")
        self._discover_dataclasses()
        print(f"    Found {len(self.dataclasses)} dataclasses")

        # Phase 2: Analyze field contracts
        print("\n[2/5] Analyzing field contracts...")
        self._analyze_field_contracts()

        # Phase 3: Check serialization contracts
        print("\n[3/5] Checking serialization contracts...")
        self._check_serialization_contracts()

        # Phase 4: Trace producer-consumer relationships
        print("\n[4/5] Tracing producer-consumer relationships...")
        self._trace_producer_consumer()

        # Phase 5: Check for divergences
        print("\n[5/5] Checking Engine→Model→Consumer divergences...")
        self._check_divergences()

        # Generate reports
        print("\nGenerating reports...")
        self._generate_contract_certification_md()
        self._generate_dataclass_matrix_md()

        # Determine verdict
        verdict = self._determine_verdict()

        print(f"\n{'=' * 60}")
        print(f"CONTRACT CERTIFICATION VERDICT: {verdict}")
        print(f"Total Findings: {len(self.findings)}")
        print(f"  FAIL: {sum(1 for f in self.findings if f.severity == 'FAIL')}")
        print(f"  WARNING: {sum(1 for f in self.findings if f.severity == 'WARNING')}")
        print(f"  INFO: {sum(1 for f in self.findings if f.severity == 'INFO')}")
        print(f"{'=' * 60}")

        return {
            "verdict": verdict,
            "total_findings": len(self.findings),
            "fail_count": sum(1 for f in self.findings if f.severity == "FAIL"),
            "warning_count": sum(1 for f in self.findings if f.severity == "WARNING"),
            "info_count": sum(1 for f in self.findings if f.severity == "INFO"),
            "dataclasses_analyzed": len(self.dataclasses),
        }

    def _discover_dataclasses(self):
        """Discover all @dataclass decorated classes in mercury_ai/."""
        ignore_dirs = {".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache", "build", "dist", "site-packages"}

        for py_file in self.mercury_ai_root.rglob("*.py"):
            if any(part in ignore_dirs for part in py_file.parts):
                continue

            try:
                source = py_file.read_text(encoding="utf-8", errors="ignore")
                tree = ast.parse(source)
            except Exception as e:
                print(f"    Warning: Failed to parse {py_file}: {e}")
                continue

            module = ".".join(py_file.relative_to(self.project_root).with_suffix("").parts)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check for @dataclass decorator
                    is_dataclass = False
                    is_frozen = False
                    decorators = []

                    for decorator in node.decorator_list:
                        dec_str = ast.unparse(decorator)
                        decorators.append(dec_str)
                        if "dataclass" in dec_str:
                            is_dataclass = True
                            if "frozen=True" in dec_str:
                                is_frozen = True

                    if not is_dataclass:
                        continue

                    # Extract fields
                    fields = []
                    has_post_init = False
                    has_to_dict = False
                    has_from_dict = False
                    methods = []

                    for item in node.body:
                        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                            # Field with type annotation
                            field_name = item.target.id
                            type_ann = ast.unparse(item.annotation) if item.annotation else "Any"
                            has_default = item.value is not None
                            default_val = ast.unparse(item.value) if item.value else ""
                            is_optional = "Optional" in type_ann or "Union" in type_ann
                            is_required = not has_default and not is_optional

                            fields.append(DataclassField(
                                name=field_name,
                                type_annotation=type_ann,
                                has_default=has_default,
                                default_value=default_val,
                                is_optional=is_optional,
                                is_required=is_required,
                                line=item.lineno
                            ))

                        elif isinstance(item, ast.FunctionDef):
                            methods.append(item.name)
                            if item.name == "__post_init__":
                                has_post_init = True
                            elif item.name == "to_dict":
                                has_to_dict = True
                            elif item.name in ("from_dict", "from_json", "deserialize"):
                                has_from_dict = True

                    has_serialization = has_to_dict or has_from_dict or has_post_init

                    # Get bases
                    bases = [ast.unparse(base) for base in node.bases]

                    dc_info = DataclassInfo(
                        name=node.name,
                        module=module,
                        file_path=str(py_file.relative_to(self.project_root)),
                        line=node.lineno,
                        is_frozen=is_frozen,
                        fields=fields,
                        has_post_init=has_post_init,
                        has_to_dict=has_to_dict,
                        has_from_dict=has_from_dict,
                        has_serialization=has_serialization,
                        decorators=decorators,
                        bases=bases,
                        methods=methods
                    )

                    self.dataclasses.append(dc_info)

    def _analyze_field_contracts(self):
        """Analyze field-level contracts for each dataclass."""
        for dc in self.dataclasses:
            # Check 1: Required fields without defaults
            required_fields = [f for f in dc.fields if f.is_required]
            for field in required_fields:
                self.findings.append(ContractFinding(
                    type="REQUIRED_FIELD_NO_DEFAULT",
                    severity="WARNING",
                    dataclass=dc.name,
                    module=dc.module,
                    field=field.name,
                    message=f"Required field '{field.name}' has no default value",
                    evidence=f"Field '{field.name}: {field.type_annotation}' at line {field.line} in {dc.file_path} is required but has no default",
                    file_path=dc.file_path,
                    line=field.line
                ))

            # Check 2: Mutable default values (list, dict, set)
            for field in dc.fields:
                if field.has_default:
                    default_lower = field.default_value.lower()
                    if default_lower in ("[]", "{}", "set()") or default_lower.startswith(("list(", "dict(", "set(")):
                        self.findings.append(ContractFinding(
                            type="MUTABLE_DEFAULT",
                            severity="FAIL",
                            dataclass=dc.name,
                            module=dc.module,
                            field=field.name,
                            message=f"Mutable default value for field '{field.name}'",
                            evidence=f"Field '{field.name}' at line {field.line} in {dc.file_path} has mutable default: {field.default_value}",
                            file_path=dc.file_path,
                            line=field.line
                        ))

            # Check 3: Optional fields without explicit None default
            for field in dc.fields:
                if field.is_optional and not field.has_default:
                    self.findings.append(ContractFinding(
                        type="OPTIONAL_NO_DEFAULT",
                        severity="INFO",
                        dataclass=dc.name,
                        module=dc.module,
                        field=field.name,
                        message=f"Optional field '{field.name}' has no explicit default (implicitly None)",
                        evidence=f"Field '{field.name}: {field.type_annotation}' at line {field.line} in {dc.file_path} is Optional but has no default",
                        file_path=dc.file_path,
                        line=field.line
                    ))

            # Check 4: Frozen dataclass with mutable fields
            if dc.is_frozen:
                for field in dc.fields:
                    type_lower = field.type_annotation.lower()
                    if any(t in type_lower for t in ["list", "dict", "set", "bytearray"]):
                        self.findings.append(ContractFinding(
                            type="FROZEN_WITH_MUTABLE_FIELD",
                            severity="WARNING",
                            dataclass=dc.name,
                            module=dc.module,
                            field=field.name,
                            message=f"Frozen dataclass has mutable field '{field.name}'",
                            evidence=f"Frozen dataclass '{dc.name}' at line {dc.line} in {dc.file_path} contains mutable field '{field.name}: {field.type_annotation}'",
                            file_path=dc.file_path,
                            line=dc.line
                        ))

            # Check 5: Field naming consistency (snake_case)
            for field in dc.fields:
                if not field.name.islower() and "_" not in field.name and field.name != field.name.lower():
                    # Check if it's not a constant (ALL_CAPS)
                    if not field.name.isupper():
                        self.findings.append(ContractFinding(
                            type="FIELD_NAMING_CONVENTION",
                            severity="INFO",
                            dataclass=dc.name,
                            module=dc.module,
                            field=field.name,
                            message=f"Field '{field.name}' may not follow snake_case convention",
                            evidence=f"Field '{field.name}' at line {field.line} in {dc.file_path} appears to use camelCase or PascalCase",
                            file_path=dc.file_path,
                            line=field.line
                        ))

    def _check_serialization_contracts(self):
        """Check serialization/deserialization contracts."""
        for dc in self.dataclasses:
            # Check 1: Dataclass with fields but no serialization methods
            if dc.fields and not dc.has_serialization:
                self.findings.append(ContractFinding(
                    type="NO_SERIALIZATION",
                    severity="WARNING",
                    dataclass=dc.name,
                    module=dc.module,
                    message=f"Dataclass has {len(dc.fields)} fields but no serialization methods",
                    evidence=f"Dataclass '{dc.name}' in {dc.file_path}:{dc.line} has fields but no __post_init__, to_dict, or from_dict methods",
                    file_path=dc.file_path,
                    line=dc.line
                ))

            # Check 2: Has to_dict but no from_dict (asymmetric serialization)
            if dc.has_to_dict and not dc.has_from_dict:
                self.findings.append(ContractFinding(
                    type="ASYMMETRIC_SERIALIZATION",
                    severity="WARNING",
                    dataclass=dc.name,
                    module=dc.module,
                    message=f"Dataclass has to_dict but no from_dict/from_json",
                    evidence=f"Dataclass '{dc.name}' in {dc.file_path}:{dc.line} can serialize but not deserialize",
                    file_path=dc.file_path,
                    line=dc.line
                ))

            # Check 3: Has from_dict but no to_dict
            if dc.has_from_dict and not dc.has_to_dict:
                self.findings.append(ContractFinding(
                    type="ASYMMETRIC_SERIALIZATION",
                    severity="WARNING",
                    dataclass=dc.name,
                    module=dc.module,
                    message=f"Dataclass has from_dict but no to_dict",
                    evidence=f"Dataclass '{dc.name}' in {dc.file_path}:{dc.line} can deserialize but not serialize",
                    file_path=dc.file_path,
                    line=dc.line
                ))

            # Check 4: __post_init__ without validation
            if dc.has_post_init:
                # We can't easily check the content without more AST analysis
                # But we can flag it for manual review
                self.findings.append(ContractFinding(
                    type="HAS_POST_INIT",
                    severity="INFO",
                    dataclass=dc.name,
                    module=dc.module,
                    message=f"Dataclass has __post_init__ - verify validation logic",
                    evidence=f"Dataclass '{dc.name}' in {dc.file_path}:{dc.line} has __post_init__ method",
                    file_path=dc.file_path,
                    line=dc.line
                ))

    def _trace_producer_consumer(self):
        """Trace producer-consumer relationships by analyzing field usage across modules."""
        # Build a map of which modules use which dataclasses
        dataclass_by_name = {dc.name: dc for dc in self.dataclasses}

        # Scan all Python files for dataclass usage (instantiation, field access)
        ignore_dirs = {".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache", "build", "dist", "site-packages"}

        for py_file in self.project_root.rglob("*.py"):
            if any(part in ignore_dirs for part in py_file.parts):
                continue

            try:
                source = py_file.read_text(encoding="utf-8", errors="ignore")
                tree = ast.parse(source)
            except Exception:
                continue

            module = ".".join(py_file.relative_to(self.project_root).with_suffix("").parts)

            for node in ast.walk(tree):
                # Check for instantiation: DataclassName(...)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    called_name = node.func.id
                    if called_name in dataclass_by_name:
                        dc = dataclass_by_name[called_name]
                        self.producer_consumer_map[dc.name].append(module)
                        for field in dc.fields:
                            self.field_usage[field.name].add(module)

                # Check for attribute access: obj.field_name
                elif isinstance(node, ast.Attribute):
                    attr_name = node.attr
                    # Track field access patterns
                    for dc_name, dc in dataclass_by_name.items():
                        field_names = [f.name for f in dc.fields]
                        if attr_name in field_names:
                            self.field_usage[attr_name].add(module)

    def _check_divergences(self):
        """Check for Engine→Model→Consumer divergences."""
        # Group dataclasses by potential role
        engine_dataclasses = [dc for dc in self.dataclasses if "engine" in dc.module.lower() or "engine" in dc.name.lower()]
        model_dataclasses = [dc for dc in self.dataclasses if "model" in dc.module.lower() or "model" in dc.name.lower()]
        consumer_modules = set()

        # Find consumer modules (those that use dataclasses but don't define them)
        for dc_name, consumers in self.producer_consumer_map.items():
            dc = next((d for d in self.dataclasses if d.name == dc_name), None)
            if dc:
                for consumer in consumers:
                    if consumer != dc.module:
                        consumer_modules.add(consumer)

        # Check 1: Engine dataclasses not consumed by models
        for engine_dc in engine_dataclasses:
            consumers = self.producer_consumer_map.get(engine_dc.name, [])
            model_consumers = [c for c in consumers if "model" in c.lower()]
            if not model_consumers and consumers:
                self.findings.append(ContractFinding(
                    type="ENGINE_NOT_CONSUMED_BY_MODEL",
                    severity="WARNING",
                    dataclass=engine_dc.name,
                    module=engine_dc.module,
                    message=f"Engine dataclass '{engine_dc.name}' not consumed by any model module",
                    evidence=f"Engine dataclass '{engine_dc.name}' in {engine_dc.module} is used by: {', '.join(consumers) if consumers else 'none'}",
                    file_path=engine_dc.file_path,
                    line=engine_dc.line
                ))

        # Check 2: Model dataclasses not consumed by consumers
        for model_dc in model_dataclasses:
            consumers = self.producer_consumer_map.get(model_dc.name, [])
            external_consumers = [c for c in consumers if c != model_dc.module]
            if not external_consumers:
                self.findings.append(ContractFinding(
                    type="MODEL_NOT_CONSUMED",
                    severity="WARNING",
                    dataclass=model_dc.name,
                    module=model_dc.module,
                    message=f"Model dataclass '{model_dc.name}' not consumed by any external module",
                    evidence=f"Model dataclass '{model_dc.name}' in {model_dc.module} has no external consumers",
                    file_path=model_dc.file_path,
                    line=model_dc.line
                ))

        # Check 3: Field access mismatches - consumers accessing fields not in dataclass
        for field_name, modules in self.field_usage.items():
            # Find which dataclasses have this field
            dcs_with_field = [dc for dc in self.dataclasses if any(f.name == field_name for f in dc.fields)]
            if not dcs_with_field:
                # Field accessed but not defined in any dataclass
                for module in modules:
                    self.findings.append(ContractFinding(
                        type="UNDEFINED_FIELD_ACCESS",
                        severity="FAIL",
                        dataclass="N/A",
                        module=module,
                        field=field_name,
                        message=f"Module accesses field '{field_name}' not defined in any dataclass",
                        evidence=f"Module '{module}' accesses attribute '{field_name}' but no dataclass defines this field",
                        file_path="",
                        line=0
                    ))

        # Check 4: Duplicate dataclass names across modules (potential divergence)
        name_to_dcs = defaultdict(list)
        for dc in self.dataclasses:
            name_to_dcs[dc.name].append(dc)

        for name, dcs in name_to_dcs.items():
            if len(dcs) > 1:
                modules = [dc.module for dc in dcs]
                # Check if fields differ
                field_sets = [set(f.name for f in dc.fields) for dc in dcs]
                if len(set(frozenset(fs) for fs in field_sets)) > 1:
                    self.findings.append(ContractFinding(
                        type="DATACLASS_FIELD_DIVERGENCE",
                        severity="FAIL",
                        dataclass=name,
                        module=", ".join(modules),
                        message=f"Dataclass '{name}' defined in multiple modules with different fields",
                        evidence=f"Dataclass '{name}' exists in {len(dcs)} modules ({', '.join(modules)}) with different field sets",
                        file_path=dcs[0].file_path,
                        line=dcs[0].line
                    ))

        # Check 5: Required fields in producer not provided by consumer
        for dc in self.dataclasses:
            required_fields = [f for f in dc.fields if f.is_required]
            consumers = self.producer_consumer_map.get(dc.name, [])
            for consumer in consumers:
                if consumer != dc.module:
                    # This is a heuristic - we can't easily verify without runtime analysis
                    # But we can flag for review
                    if required_fields:
                        self.findings.append(ContractFinding(
                            type="REQUIRED_FIELDS_NEED_VERIFICATION",
                            severity="INFO",
                            dataclass=dc.name,
                            module=dc.module,
                            message=f"Dataclass '{dc.name}' has {len(required_fields)} required fields - verify consumer provides all",
                            evidence=f"Required fields: {[f.name for f in required_fields]}. Consumer: {consumer}",
                            file_path=dc.file_path,
                            line=dc.line
                        ))

    def _determine_verdict(self) -> str:
        """Determine overall verdict: PASS, WARNING, or FAIL."""
        fail_count = sum(1 for f in self.findings if f.severity == "FAIL")
        warning_count = sum(1 for f in self.findings if f.severity == "WARNING")

        if fail_count > 0:
            return "FAIL"
        elif warning_count > 10:
            return "WARNING"
        elif warning_count > 0:
            return "WARNING"
        else:
            return "PASS"

    def _generate_contract_certification_md(self):
        """Generate CONTRACT_CERTIFICATION.md report."""
        verdict = self._determine_verdict()

        # Group findings by type
        by_type = defaultdict(list)
        for f in self.findings:
            by_type[f.type].append(f)

        lines = []
        lines.append("# CONTRACT CERTIFICATION REPORT")
        lines.append("")
        lines.append(f"**Project:** Mercury AI V1")
        lines.append(f"**Audit:** SPRINT 1.9 BLOCO 2/10 - Contract Certification")
        lines.append(f"**Verdict:** {verdict}")
        lines.append(f"**Total Findings:** {len(self.findings)}")
        lines.append(f"**FAIL:** {sum(1 for f in self.findings if f.severity == 'FAIL')}")
        lines.append(f"**WARNING:** {sum(1 for f in self.findings if f.severity == 'WARNING')}")
        lines.append(f"**INFO:** {sum(1 for f in self.findings if f.severity == 'INFO')}")
        lines.append(f"**Dataclasses Analyzed:** {len(self.dataclasses)}")
        lines.append("")

        # Summary table
        lines.append("## Summary by Category")
        lines.append("")
        lines.append("| Category | Count | Severity |")
        lines.append("|----------|-------|----------|")
        for ftype, items in sorted(by_type.items()):
            severities = set(i.severity for i in items)
            sev_str = ", ".join(sorted(severities))
            lines.append(f"| {ftype} | {len(items)} | {sev_str} |")
        lines.append("")

        # Dataclass summary
        lines.append("## Dataclass Inventory")
        lines.append("")
        lines.append("| Dataclass | Module | Fields | Frozen | Serialization |")
        lines.append("|-----------|--------|--------|--------|---------------|")
        for dc in sorted(self.dataclasses, key=lambda x: (x.module, x.name)):
            ser = []
            if dc.has_post_init:
                ser.append("__post_init__")
            if dc.has_to_dict:
                ser.append("to_dict")
            if dc.has_from_dict:
                ser.append("from_dict")
            ser_str = ", ".join(ser) if ser else "None"
            lines.append(f"| {dc.name} | {dc.module} | {len(dc.fields)} | {dc.is_frozen} | {ser_str} |")
        lines.append("")

        # Detailed findings
        lines.append("## Detailed Findings")
        lines.append("")

        for ftype, items in sorted(by_type.items()):
            lines.append(f"### {ftype} ({len(items)} findings)")
            lines.append("")
            for item in items:
                lines.append(f"#### {item.severity}: {item.dataclass} ({item.module})")
                lines.append("")
                if item.field:
                    lines.append(f"**Field:** {item.field}")
                lines.append(f"**Message:** {item.message}")
                lines.append("")
                lines.append(f"**Evidence:** {item.evidence}")
                lines.append("")
                if item.file_path:
                    lines.append(f"**Location:** {item.file_path}:{item.line}")
                lines.append("")

        # Write report
        report_path = self.output_dir / "CONTRACT_CERTIFICATION.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Generated: {report_path}")

    def _generate_dataclass_matrix_md(self):
        """Generate DATACLASS_MATRIX.md with detailed field matrix."""
        lines = []
        lines.append("# DATACLASS CONTRACT MATRIX")
        lines.append("")
        lines.append(f"**Project:** Mercury AI V1")
        lines.append(f"**Audit:** SPRINT 1.9 BLOCO 2/10 - Contract Certification")
        lines.append(f"**Generated:** {datetime.now().isoformat()}")
        lines.append(f"**Total Dataclasses:** {len(self.dataclasses)}")
        lines.append("")

        # Producer-Consumer Matrix
        lines.append("## Producer-Consumer Matrix")
        lines.append("")
        lines.append("| Dataclass | Producer Module | Consumer Modules | Field Count |")
        lines.append("|-----------|-----------------|------------------|-------------|")
        for dc in sorted(self.dataclasses, key=lambda x: (x.module, x.name)):
            consumers = self.producer_consumer_map.get(dc.name, [])
            external_consumers = [c for c in consumers if c != dc.module]
            lines.append(f"| {dc.name} | {dc.module} | {', '.join(external_consumers) if external_consumers else 'None'} | {len(dc.fields)} |")
        lines.append("")

        # Field Matrix
        lines.append("## Field Contract Matrix")
        lines.append("")
        lines.append("| Dataclass | Field | Type | Required | Optional | Default | Frozen | Line |")
        lines.append("|-----------|-------|------|----------|----------|---------|--------|------|")
        for dc in sorted(self.dataclasses, key=lambda x: (x.module, x.name)):
            for field in dc.fields:
                req = "✓" if field.is_required else ""
                opt = "✓" if field.is_optional else ""
                default = field.default_value if field.has_default else ""
                lines.append(f"| {dc.name} | {field.name} | {field.type_annotation} | {req} | {opt} | {default} | {dc.is_frozen} | {field.line} |")
        lines.append("")

        # Serialization Matrix
        lines.append("## Serialization Contract Matrix")
        lines.append("")
        lines.append("| Dataclass | __post_init__ | to_dict | from_dict | Asymmetric |")
        lines.append("|-----------|---------------|---------|-----------|------------|")
        for dc in sorted(self.dataclasses, key=lambda x: (x.module, x.name)):
            asymmetric = "⚠️" if (dc.has_to_dict != dc.has_from_dict) and (dc.has_to_dict or dc.has_from_dict) else ""
            lines.append(f"| {dc.name} | {'✓' if dc.has_post_init else ''} | {'✓' if dc.has_to_dict else ''} | {'✓' if dc.has_from_dict else ''} | {asymmetric} |")
        lines.append("")

        # Field Usage Across Modules
        lines.append("## Field Usage Across Modules")
        lines.append("")
        lines.append("| Field | Defined In | Used In Modules |")
        lines.append("|-------|------------|-----------------|")
        for field_name, modules in sorted(self.field_usage.items()):
            # Find defining dataclasses
            defining = [dc.name for dc in self.dataclasses if any(f.name == field_name for f in dc.fields)]
            lines.append(f"| {field_name} | {', '.join(defining) if defining else 'N/A'} | {', '.join(sorted(modules))} |")
        lines.append("")

        # Write report
        report_path = self.output_dir / "DATACLASS_MATRIX.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Generated: {report_path}")


def main():
    """Main entry point."""
    auditor = ContractCertificationAuditor()
    result = auditor.run()

    # Exit with appropriate code
    if result["verdict"] == "FAIL":
        exit(1)
    elif result["verdict"] == "WARNING":
        exit(2)
    else:
        exit(0)


if __name__ == "__main__":
    main()
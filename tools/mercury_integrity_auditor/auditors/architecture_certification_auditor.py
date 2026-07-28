"""
Architecture Certification Auditor - SPRINT 1.9 BLOCO 1/10
Mercury AI V1 Architecture Certification

Audits:
- Broken imports
- Circular imports
- Orphan modules
- Duplicate engines/models/dataclasses
- Unused functions/classes
- Hidden/dead dependencies
- SOLID violations (SRP, DIP, OCP, LSP)
- Excessive coupling
- Dead code

Generates:
- ARCHITECTURE_CERTIFICATION.md
- DEPENDENCY_GRAPH_V2.json
- ORPHAN_MODULES.md

Emits: PASS / WARNING / FAIL verdict
"""

import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any


class ArchitectureCertificationAuditor:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.mercury_dir = project_root / ".mercury"
        self.output_dir = project_root / ".mercury" / "audits"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load base data
        self.imports = self._load_json("imports.json")
        self.classes = self._load_json("classes.json")
        self.functions = self._load_json("functions.json")
        self.dependency_graph = self._load_json("dependency_graph.json")
        self.call_graph = self._load_json("call_graph.json")
        self.scan_report = self._load_json("scan_report.json")

        # Build indices
        self.module_to_imports = defaultdict(list)
        self.module_to_classes = defaultdict(list)
        self.module_to_functions = defaultdict(list)
        self.all_modules = set()
        self.external_imports = set()
        self.internal_imports = defaultdict(set)

        self._build_indices()

    def _load_json(self, filename: str) -> Any:
        path = self.mercury_dir / filename
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return [] if filename != "dependency_graph.json" else {}

    def _build_indices(self):
        """Build lookup indices from loaded data."""
        for imp in self.imports:
            module = imp.get("module", "")
            import_name = imp.get("import", "")
            self.module_to_imports[module].append(import_name)
            self.all_modules.add(module)

            # Classify as internal or external
            if import_name.startswith("mercury_ai.") or import_name.startswith("app."):
                self.internal_imports[module].add(import_name)
            else:
                self.external_imports.add(import_name)

        for cls in self.classes:
            module = cls.get("module", "")
            self.module_to_classes[module].append(cls)
            self.all_modules.add(module)

        for func in self.functions:
            module = func.get("module", "")
            self.module_to_functions[module].append(func)
            self.all_modules.add(module)

        # Add modules from dependency graph
        for module in self.dependency_graph:
            self.all_modules.add(module)

    def run(self) -> dict:
        """Run the complete architecture certification audit."""
        print("----------------------------------")
        print("Architecture Certification Audit")
        print("----------------------------------")

        findings = []

        # 1. Broken imports
        findings.extend(self._audit_broken_imports())

        # 2. Circular imports
        findings.extend(self._audit_circular_imports())

        # 3. Orphan modules
        findings.extend(self._audit_orphan_modules())

        # 4. Duplicate engines/models/dataclasses
        findings.extend(self._audit_duplicates())

        # 5. Unused functions/classes
        findings.extend(self._audit_unused())

        # 6. Hidden/dead dependencies
        findings.extend(self._audit_hidden_dependencies())

        # 7. SOLID violations
        findings.extend(self._audit_solid_violations())

        # 8. Excessive coupling
        findings.extend(self._audit_excessive_coupling())

        # 9. Dead code
        findings.extend(self._audit_dead_code())

        # Generate deliverables
        self._generate_architecture_certification_md(findings)
        self._generate_dependency_graph_v2()
        self._generate_orphan_modules_md(findings)

        # Determine verdict
        verdict = self._determine_verdict(findings)

        print(f"Total findings: {len(findings)}")
        print(f"Verdict: {verdict}")
        print("----------------------------------")

        return {
            "verdict": verdict,
            "findings_count": len(findings),
            "findings": findings,
        }

    def _audit_broken_imports(self) -> list:
        """Audit for broken imports - imports that cannot be resolved."""
        findings = []

        # Get all valid internal modules
        valid_modules = set()
        for module in self.all_modules:
            if module.startswith("mercury_ai.") or module.startswith("app."):
                valid_modules.add(module)

        # Check each import
        for module, imports in self.module_to_imports.items():
            for imp in imports:
                if imp.startswith("mercury_ai.") or imp.startswith("app."):
                    # Check if the imported module exists
                    if imp not in valid_modules:
                        # Check if it's a submodule that might exist
                        found = False
                        for valid in valid_modules:
                            if valid.startswith(imp + ".") or valid == imp:
                                found = True
                                break
                        if not found:
                            findings.append({
                                "type": "BROKEN_IMPORT",
                                "severity": "FAIL",
                                "module": module,
                                "import": imp,
                                "message": f"Broken import: '{imp}' not found in codebase",
                                "evidence": f"Module '{module}' imports '{imp}' which does not exist"
                            })

        return findings

    def _audit_circular_imports(self) -> list:
        """Detect circular import dependencies."""
        findings = []

        # Build adjacency list
        graph = defaultdict(set)
        for module, deps in self.dependency_graph.items():
            for dep in deps:
                if dep.startswith("mercury_ai.") or dep.startswith("app."):
                    graph[module].add(dep)

        # Tarjan's algorithm for strongly connected components
        index = 0
        stack = []
        on_stack = set()
        indices = {}
        lowlinks = {}
        sccs = []

        def strongconnect(v):
            nonlocal index
            indices[v] = index
            lowlinks[v] = index
            index += 1
            stack.append(v)
            on_stack.add(v)

            for w in graph.get(v, []):
                if w not in indices:
                    strongconnect(w)
                    lowlinks[v] = min(lowlinks[v], lowlinks[w])
                elif w in on_stack:
                    lowlinks[v] = min(lowlinks[v], indices[w])

            if lowlinks[v] == indices[v]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack.remove(w)
                    scc.append(w)
                    if w == v:
                        break
                if len(scc) > 1:
                    sccs.append(scc)

        for v in graph:
            if v not in indices:
                strongconnect(v)

        for scc in sccs:
            findings.append({
                "type": "CIRCULAR_IMPORT",
                "severity": "FAIL",
                "modules": scc,
                "message": f"Circular import detected among {len(scc)} modules",
                "evidence": " -> ".join(scc) + " -> " + scc[0]
            })

        return findings

    def _audit_orphan_modules(self) -> list:
        """Find orphan modules - modules that are not imported by anyone."""
        findings = []

        # Find all modules that are imported by others
        imported_modules = set()
        for module, deps in self.dependency_graph.items():
            for dep in deps:
                if dep.startswith("mercury_ai.") or dep.startswith("app."):
                    imported_modules.add(dep)

        # Also check internal imports
        for module, imports in self.internal_imports.items():
            for imp in imports:
                imported_modules.add(imp)

        # Find orphans (internal modules not imported by anyone)
        internal_modules = {m for m in self.all_modules if m.startswith("mercury_ai.") or m.startswith("app.")}

        # Exclude entry points (main, scripts, tests)
        entry_points = {
            "main", "run_instrumented", "run_deterministic_replay_scenarios",
            "run_institutional_replay", "calculate_institutional_stats",
            "parity_check", "resolve_merge_conflicts"
        }

        orphans = []
        for module in internal_modules:
            if module not in imported_modules and module not in entry_points:
                # Check if it has any classes/functions that might be used via dynamic import
                has_content = bool(self.module_to_classes.get(module) or self.module_to_functions.get(module))
                if has_content:
                    orphans.append(module)

        for orphan in sorted(orphans):
            findings.append({
                "type": "ORPHAN_MODULE",
                "severity": "WARNING",
                "module": orphan,
                "message": f"Orphan module: '{orphan}' is not imported by any other module",
                "evidence": f"Module '{orphan}' has {len(self.module_to_classes.get(orphan, []))} classes and {len(self.module_to_functions.get(orphan, []))} functions but zero inbound imports"
            })

        return findings

    def _audit_duplicates(self) -> list:
        """Find duplicate engines/models/dataclasses by name."""
        findings = []

        # Group classes by name
        class_by_name = defaultdict(list)
        for cls in self.classes:
            class_by_name[cls["name"]].append(cls)

        # Group functions by name
        func_by_name = defaultdict(list)
        for func in self.functions:
            func_by_name[func["name"]].append(func)

        # Check for duplicate class names (potential duplicate engines/models)
        for name, instances in class_by_name.items():
            if len(instances) > 1:
                modules = [i["module"] for i in instances]
                # Check if they're in different modules (true duplication)
                if len(set(modules)) > 1:
                    findings.append({
                        "type": "DUPLICATE_CLASS",
                        "severity": "WARNING",
                        "name": name,
                        "modules": modules,
                        "message": f"Duplicate class name '{name}' found in {len(modules)} modules",
                        "evidence": f"Class '{name}' defined in: {', '.join(modules)}"
                    })

        # Check for duplicate function names
        for name, instances in func_by_name.items():
            if len(instances) > 1:
                modules = [i["module"] for i in instances]
                if len(set(modules)) > 1:
                    findings.append({
                        "type": "DUPLICATE_FUNCTION",
                        "severity": "WARNING",
                        "name": name,
                        "modules": modules,
                        "message": f"Duplicate function name '{name}' found in {len(modules)} modules",
                        "evidence": f"Function '{name}' defined in: {', '.join(modules)}"
                    })

        return findings

    def _audit_unused(self) -> list:
        """Find unused functions/classes."""
        findings = []

        # Build call graph lookup
        called_functions = set()
        for call in self.call_graph:
            called_functions.add(call.get("call", ""))

        # Check functions
        for module, funcs in self.module_to_functions.items():
            for func in funcs:
                func_name = func["name"]
                # Skip dunder methods, entry points, and test functions
                if func_name.startswith("__") or func_name.startswith("test_"):
                    continue
                if func_name in ["main", "run", "execute"]:
                    continue

                # Check if function is called anywhere
                full_name = f"{module}.{func_name}"
                simple_called = func_name in called_functions
                full_called = full_name in called_functions

                if not simple_called and not full_called:
                    findings.append({
                        "type": "UNUSED_FUNCTION",
                        "severity": "WARNING",
                        "module": module,
                        "name": func_name,
                        "line": func.get("line", 0),
                        "message": f"Unused function: '{func_name}' in '{module}'",
                        "evidence": f"Function '{func_name}' at line {func.get('line', 0)} in '{module}' is never called"
                    })

        # Check classes (instantiation via call graph)
        instantiated_classes = set()
        for call in self.call_graph:
            call_target = call.get("call", "")
            # Check if it looks like a class instantiation
            for cls in self.classes:
                if cls["name"] in call_target:
                    instantiated_classes.add(cls["name"])

        for module, classes in self.module_to_classes.items():
            for cls in classes:
                cls_name = cls["name"]
                if cls_name not in instantiated_classes:
                    # Check if it's used as base class
                    used_as_base = False
                    for other_cls in self.classes:
                        for base in other_cls.get("bases", []):
                            if cls_name in base:
                                used_as_base = True
                                break
                    if not used_as_base:
                        findings.append({
                            "type": "UNUSED_CLASS",
                            "severity": "WARNING",
                            "module": module,
                            "name": cls_name,
                            "line": cls.get("line", 0),
                            "message": f"Unused class: '{cls_name}' in '{module}'",
                            "evidence": f"Class '{cls_name}' at line {cls.get('line', 0)} in '{module}' is never instantiated or inherited"
                        })

        return findings

    def _audit_hidden_dependencies(self) -> list:
        """Find hidden/dead dependencies - imports that are declared but never used."""
        findings = []

        # For each module, check if imports are actually used in the code
        # This is a simplified check - we look at call graph and class usage
        used_names = set()
        for call in self.call_graph:
            used_names.add(call.get("call", ""))

        for cls in self.classes:
            used_names.add(cls["name"])
            for base in cls.get("bases", []):
                used_names.add(base)

        for module, imports in self.module_to_imports.items():
            for imp in imports:
                # Extract the last part of the import
                parts = imp.split(".")
                last_part = parts[-1]

                # Check if this import is used
                is_used = False
                if last_part in used_names:
                    is_used = True
                # Check if any part of the import path is used
                for part in parts:
                    if part in used_names:
                        is_used = True
                        break

                if not is_used and (imp.startswith("mercury_ai.") or imp.startswith("app.")):
                    findings.append({
                        "type": "HIDDEN_DEPENDENCY",
                        "severity": "WARNING",
                        "module": module,
                        "import": imp,
                        "message": f"Potentially unused import: '{imp}' in '{module}'",
                        "evidence": f"Import '{imp}' in module '{module}' does not appear to be used in call graph or class hierarchy"
                    })

        return findings

    def _audit_solid_violations(self) -> list:
        """Audit for SOLID principle violations."""
        findings = []

        # SRP (Single Responsibility Principle) - classes with too many methods
        for module, classes in self.module_to_classes.items():
            for cls in classes:
                cls_name = cls["name"]
                # Count methods in this class (approximate via functions in same module)
                method_count = 0
                for func in self.module_to_functions.get(module, []):
                    # Heuristic: functions that might be methods
                    if func["name"].startswith(cls_name.lower() + "_") or func["name"] in ["execute", "run", "process", "analyze", "validate", "calculate", "generate", "build", "create", "update", "delete", "get", "set", "load", "save", "export", "import"]:
                        method_count += 1

                if method_count > 15:
                    findings.append({
                        "type": "SRP_VIOLATION",
                        "severity": "WARNING",
                        "module": module,
                        "class": cls_name,
                        "method_count": method_count,
                        "message": f"SRP violation: Class '{cls_name}' has ~{method_count} methods (exceeds 15)",
                        "evidence": f"Class '{cls_name}' in '{module}' appears to have {method_count} methods, suggesting multiple responsibilities"
                    })

        # DIP (Dependency Inversion Principle) - high-level modules depending on low-level concretions
        for module, deps in self.dependency_graph.items():
            if module.startswith("mercury_ai.core.") or module.startswith("mercury_ai.brain."):
                # High-level modules
                for dep in deps:
                    if dep.startswith("mercury_ai.providers.") or dep.startswith("mercury_ai.database.") or dep.startswith("mercury_ai.market."):
                        findings.append({
                            "type": "DIP_VIOLATION",
                            "severity": "WARNING",
                            "module": module,
                            "depends_on": dep,
                            "message": f"DIP violation: High-level module '{module}' depends on low-level '{dep}'",
                            "evidence": f"Core/brain module '{module}' directly depends on provider/database/market implementation '{dep}'"
                        })

        # OCP (Open/Closed Principle) - classes that are not open for extension
        # Look for classes with no inheritance (no subclasses)
        class_children = defaultdict(list)
        for cls in self.classes:
            for base in cls.get("bases", []):
                for part in base.split("."):
                    if part in [c["name"] for c in self.classes]:
                        class_children[part].append(cls["name"])

        for module, classes in self.module_to_classes.items():
            for cls in classes:
                cls_name = cls["name"]
                if cls_name not in class_children and not cls.get("bases"):
                    # Class has no children and no parents - might be closed
                    if len(self.module_to_functions.get(module, [])) > 5:
                        findings.append({
                            "type": "OCP_VIOLATION",
                            "severity": "INFO",
                            "module": module,
                            "class": cls_name,
                            "message": f"OCP concern: Class '{cls_name}' has no inheritance hierarchy",
                            "evidence": f"Class '{cls_name}' in '{module}' has no subclasses and no base classes, limiting extensibility"
                        })

        # LSP (Liskov Substitution Principle) - check for problematic overrides
        # This is hard to detect statically, but we can flag classes with same method names in hierarchy
        for cls in self.classes:
            for base in cls.get("bases", []):
                base_name = base.split(".")[-1]
                # Find base class
                base_cls = None
                for c in self.classes:
                    if c["name"] == base_name:
                        base_cls = c
                        break
                if base_cls:
                    # Check for method name overlap (simplified)
                    base_methods = set()
                    for func in self.module_to_functions.get(base_cls["module"], []):
                        base_methods.add(func["name"])
                    child_methods = set()
                    for func in self.module_to_functions.get(cls["module"], []):
                        child_methods.add(func["name"])
                    overlap = base_methods & child_methods
                    if overlap:
                        findings.append({
                            "type": "LSP_CONCERN",
                            "severity": "INFO",
                            "module": cls["module"],
                            "class": cls["name"],
                            "base_class": base_name,
                            "overlapping_methods": list(overlap)[:5],
                            "message": f"LSP concern: Class '{cls['name']}' overrides {len(overlap)} methods from '{base_name}'",
                            "evidence": f"Class '{cls['name']}' in '{cls['module']}' overrides methods: {', '.join(list(overlap)[:5])}"
                        })

        return findings

    def _audit_excessive_coupling(self) -> list:
        """Audit for excessive coupling - modules with too many dependencies."""
        findings = []

        # Calculate fan-in and fan-out for each module
        fan_out = defaultdict(int)
        fan_in = defaultdict(int)

        for module, deps in self.dependency_graph.items():
            internal_deps = [d for d in deps if d.startswith("mercury_ai.") or d.startswith("app.")]
            fan_out[module] = len(internal_deps)
            for dep in internal_deps:
                fan_in[dep] += 1

        # Flag modules with high fan-out (too many dependencies)
        for module, count in fan_out.items():
            if count > 20:
                findings.append({
                    "type": "EXCESSIVE_COUPLING_FANOUT",
                    "severity": "WARNING",
                    "module": module,
                    "fan_out": count,
                    "message": f"Excessive coupling: Module '{module}' has fan-out of {count} (exceeds 20)",
                    "evidence": f"Module '{module}' depends on {count} internal modules"
                })

        # Flag modules with high fan-in (too many dependents - god module)
        for module, count in fan_in.items():
            if count > 15:
                findings.append({
                    "type": "EXCESSIVE_COUPLING_FANIN",
                    "severity": "WARNING",
                    "module": module,
                    "fan_in": count,
                    "message": f"God module: Module '{module}' has fan-in of {count} (exceeds 15)",
                    "evidence": f"Module '{module}' is depended upon by {count} other modules"
                })

        return findings

    def _audit_dead_code(self) -> list:
        """Audit for dead code - unreachable code paths."""
        findings = []

        # Check for modules with no entry points and no imports
        for module in self.all_modules:
            if module.startswith("mercury_ai.") or module.startswith("app."):
                # Check if it's an entry point
                is_entry = module in {
                    "main", "run_instrumented", "run_deterministic_replay_scenarios",
                    "run_institutional_replay", "calculate_institutional_stats",
                    "parity_check", "resolve_merge_conflicts"
                }

                # Check if imported
                imported = module in self.internal_imports or any(
                    module in deps for deps in self.dependency_graph.values()
                )

                # Check if has classes/functions
                has_content = bool(self.module_to_classes.get(module) or self.module_to_functions.get(module))

                if not is_entry and not imported and has_content:
                    findings.append({
                        "type": "DEAD_CODE_MODULE",
                        "severity": "WARNING",
                        "module": module,
                        "message": f"Dead code: Module '{module}' is unreachable",
                        "evidence": f"Module '{module}' has content but is not an entry point and not imported by any module"
                    })

        # Check for functions after return/raise (simplified - would need AST analysis)
        # This is a placeholder for more sophisticated analysis

        return findings

    def _determine_verdict(self, findings: list) -> str:
        """Determine overall verdict: PASS, WARNING, or FAIL."""
        fail_count = sum(1 for f in findings if f["severity"] == "FAIL")
        warning_count = sum(1 for f in findings if f["severity"] == "WARNING")

        if fail_count > 0:
            return "FAIL"
        elif warning_count > 10:
            return "WARNING"
        elif warning_count > 0:
            return "WARNING"
        else:
            return "PASS"

    def _generate_architecture_certification_md(self, findings: list):
        """Generate ARCHITECTURE_CERTIFICATION.md report."""
        verdict = self._determine_verdict(findings)

        # Group findings by type
        by_type = defaultdict(list)
        for f in findings:
            by_type[f["type"]].append(f)

        lines = []
        lines.append("# ARCHITECTURE CERTIFICATION REPORT")
        lines.append("")
        lines.append(f"**Project:** Mercury AI V1")
        lines.append(f"**Audit:** SPRINT 1.9 BLOCO 1/10 - Architecture Certification")
        lines.append(f"**Verdict:** {verdict}")
        lines.append(f"**Total Findings:** {len(findings)}")
        lines.append(f"**FAIL:** {sum(1 for f in findings if f['severity'] == 'FAIL')}")
        lines.append(f"**WARNING:** {sum(1 for f in findings if f['severity'] == 'WARNING')}")
        lines.append(f"**INFO:** {sum(1 for f in findings if f['severity'] == 'INFO')}")
        lines.append("")

        # Summary table
        lines.append("## Summary by Category")
        lines.append("")
        lines.append("| Category | Count | Severity |")
        lines.append("|----------|-------|----------|")
        for ftype, items in sorted(by_type.items()):
            severities = set(i["severity"] for i in items)
            sev_str = ", ".join(sorted(severities))
            lines.append(f"| {ftype} | {len(items)} | {sev_str} |")
        lines.append("")

        # Detailed findings
        lines.append("## Detailed Findings")
        lines.append("")

        for ftype, items in sorted(by_type.items()):
            lines.append(f"### {ftype} ({len(items)} findings)")
            lines.append("")
            for item in items:
                lines.append(f"#### {item['severity']}: {item.get('module', item.get('name', 'N/A'))}")
                lines.append("")
                lines.append(f"**Message:** {item['message']}")
                lines.append("")
                lines.append(f"**Evidence:** {item['evidence']}")
                lines.append("")
                for key, value in item.items():
                    if key not in ["type", "severity", "message", "evidence", "module", "name"]:
                        lines.append(f"**{key}:** {value}")
                lines.append("")

        # Write report
        report_path = self.output_dir / "ARCHITECTURE_CERTIFICATION.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Generated: {report_path}")

    def _generate_dependency_graph_v2(self):
        """Generate DEPENDENCY_GRAPH_V2.json with enhanced metadata."""
        # Build enhanced graph
        nodes = []
        edges = []

        # Add all modules as nodes
        for module in sorted(self.all_modules):
            node_type = "external"
            if module.startswith("mercury_ai."):
                node_type = "internal"
            elif module.startswith("app."):
                node_type = "app"
            elif module in ["main", "run_instrumented", "run_deterministic_replay_scenarios",
                           "run_institutional_replay", "calculate_institutional_stats",
                           "parity_check", "resolve_merge_conflicts"]:
                node_type = "entry_point"

            node = {
                "id": module,
                "type": node_type,
                "classes": len(self.module_to_classes.get(module, [])),
                "functions": len(self.module_to_functions.get(module, [])),
                "imports": len(self.module_to_imports.get(module, [])),
                "fan_out": len([d for d in self.dependency_graph.get(module, []) if d.startswith("mercury_ai.") or d.startswith("app.")]),
                "fan_in": 0  # Will calculate below
            }
            nodes.append(node)

        # Calculate fan-in
        fan_in = defaultdict(int)
        for module, deps in self.dependency_graph.items():
            for dep in deps:
                if dep.startswith("mercury_ai.") or dep.startswith("app."):
                    fan_in[dep] += 1

        for node in nodes:
            node["fan_in"] = fan_in.get(node["id"], 0)

        # Add edges
        for module, deps in self.dependency_graph.items():
            for dep in deps:
                if dep.startswith("mercury_ai.") or dep.startswith("app."):
                    edges.append({
                        "source": module,
                        "target": dep,
                        "type": "import"
                    })

        # Add call graph edges (sample)
        for call in self.call_graph[:1000]:  # Limit to avoid huge file
            edges.append({
                "source": call.get("module", ""),
                "target": call.get("call", ""),
                "type": "call",
                "line": call.get("line", 0)
            })

        graph_v2 = {
            "metadata": {
                "project": "Mercury AI V1",
                "generated": "SPRINT 1.9 BLOCO 1/10",
                "total_modules": len(nodes),
                "total_edges": len(edges),
                "internal_modules": sum(1 for n in nodes if n["type"] == "internal"),
                "app_modules": sum(1 for n in nodes if n["type"] == "app"),
                "entry_points": sum(1 for n in nodes if n["type"] == "entry_point"),
            },
            "nodes": nodes,
            "edges": edges
        }

        output_path = self.output_dir / "DEPENDENCY_GRAPH_V2.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(graph_v2, f, indent=2, ensure_ascii=False)

        print(f"Generated: {output_path}")

    def _generate_orphan_modules_md(self, findings: list):
        """Generate ORPHAN_MODULES.md report."""
        orphan_findings = [f for f in findings if f["type"] == "ORPHAN_MODULE"]

        lines = []
        lines.append("# ORPHAN MODULES REPORT")
        lines.append("")
        lines.append(f"**Project:** Mercury AI V1")
        lines.append(f"**Audit:** SPRINT 1.9 BLOCO 1/10 - Architecture Certification")
        lines.append(f"**Total Orphan Modules:** {len(orphan_findings)}")
        lines.append("")

        if orphan_findings:
            lines.append("## Orphan Modules")
            lines.append("")
            lines.append("| Module | Classes | Functions | Evidence |")
            lines.append("|--------|---------|-----------|----------|")
            for item in sorted(orphan_findings, key=lambda x: x["module"]):
                module = item["module"]
                classes = len(self.module_to_classes.get(module, []))
                functions = len(self.module_to_functions.get(module, []))
                evidence = item["evidence"]
                lines.append(f"| {module} | {classes} | {functions} | {evidence} |")
            lines.append("")

            lines.append("## Recommendations")
            lines.append("")
            lines.append("1. **Review each orphan module** - Determine if it should be integrated, deprecated, or removed")
            lines.append("2. **Check for dynamic imports** - Some modules may be loaded via importlib or plugin systems")
            lines.append("3. **Verify test coverage** - Orphan modules may be test utilities or fixtures")
            lines.append("4. **Consider consolidation** - Similar functionality may exist elsewhere")
        else:
            lines.append("No orphan modules detected.")
            lines.append("")

        output_path = self.output_dir / "ORPHAN_MODULES.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Generated: {output_path}")


def main():
    project_root = Path(__file__).parent.parent.parent.parent
    auditor = ArchitectureCertificationAuditor(project_root)
    result = auditor.run()

    print(f"\nFinal Verdict: {result['verdict']}")
    print(f"Total Findings: {result['findings_count']}")

    return result["verdict"]


if __name__ == "__main__":
    main()
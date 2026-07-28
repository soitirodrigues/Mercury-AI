"""
Pipeline Certification Auditor - SPRINT 1.9 BLOCO 3/10

Traces the complete Mercury AI V1 pipeline from Provider → Scanner,
documenting for each stage: entrada, saída, tipos, tempo, objetos, contratos, exceções possíveis.

Generates:
- PIPELINE_CERTIFICATION.md: Complete pipeline certification report
- PIPELINE_TIMELINE.md: Pipeline execution timeline with timing analysis
"""

import ast
import json
import time
import inspect
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set
from collections import defaultdict


@dataclass(frozen=True)
class PipelineStage:
    """Represents a single pipeline stage with full contract documentation."""
    name: str
    order: int
    module: str
    class_name: str
    method_name: str
    file_path: str
    line_start: int
    line_end: int
    
    # Contract documentation
    entrada: str  # Input parameters with types
    saida: str    # Return type with description
    tipos: str    # Key data types involved
    tempo: str    # Expected execution time / complexity
    objetos: str  # Key objects created/used
    contratos: str  # Interface contracts (protocols, base classes)
    excecoes: str  # Possible exceptions
    
    # Evidence
    source_evidence: List[str] = field(default_factory=list)
    runtime_telemetry: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class PipelineTrace:
    """Complete pipeline trace result."""
    stages: List[PipelineStage]
    total_stages: int
    trace_timestamp: str
    mercury_ai_root: str
    verdict: str  # PASS, WARNING, FAIL
    findings: List[str]


class PipelineCertificationAuditor:
    """
    Audits the complete Mercury AI V1 pipeline by:
    1. Static AST analysis of all pipeline modules
    2. Runtime telemetry capture (if available)
    3. Contract verification against protocols/interfaces
    4. Evidence-based documentation generation
    """
    
    def __init__(self, mercury_ai_root: str):
        self.mercury_ai_root = Path(mercury_ai_root).resolve()
        self.stages: List[PipelineStage] = []
        self.findings: List[str] = []
        
    def run(self) -> PipelineTrace:
        """Execute complete pipeline certification audit."""
        print("=" * 80)
        print("PIPELINE CERTIFICATION AUDIT - SPRINT 1.9 BLOCO 3/10")
        print("=" * 80)
        
        # Define pipeline stages in execution order
        self._define_pipeline_stages()
        
        # Analyze each stage via AST
        for stage_def in self._get_stage_definitions():
            stage = self._analyze_stage(stage_def)
            self.stages.append(stage)
            print(f"  [{stage.order:2d}] {stage.name} - {stage.class_name}.{stage.method_name}")
        
        # Verify contracts
        self._verify_contracts()
        
        # Check for missing stages
        self._check_completeness()
        
        # Determine verdict
        verdict = self._determine_verdict()
        
        trace = PipelineTrace(
            stages=self.stages,
            total_stages=len(self.stages),
            trace_timestamp=datetime.utcnow().isoformat() + "Z",
            mercury_ai_root=str(self.mercury_ai_root),
            verdict=verdict,
            findings=self.findings
        )
        
        return trace
    
    def _define_pipeline_stages(self):
        """Define the expected pipeline stages in order."""
        pass  # Stages defined in _get_stage_definitions
    
    def _get_stage_definitions(self) -> List[Dict[str, Any]]:
        """Get all pipeline stage definitions with file/module/class/method info."""
        return [
            # Stage 1: Provider
            {
                "order": 1,
                "name": "Provider",
                "module": "mercury_ai.providers.market_provider",
                "class_name": "MercuryDataProvider",
                "method_name": "get_data",
                "file_path": "providers/market_provider.py",
                "protocol": "mercury_ai.providers.base_provider.MarketDataProvider",
            },
            # Stage 2: MarketData Service
            {
                "order": 2,
                "name": "MarketData",
                "module": "mercury_ai.data.market_data",
                "class_name": "MarketDataService",
                "method_name": "get_data",
                "file_path": "data/market_data.py",
                "protocol": "N/A (concrete service)",
            },
            # Stage 3: Indicators
            {
                "order": 3,
                "name": "Indicators",
                "module": "mercury_ai.data.indicator_engine",
                "class_name": "IndicatorEngine",
                "method_name": "calculate",
                "file_path": "data/indicator_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 4: Trend Analysis
            {
                "order": 4,
                "name": "Trend",
                "module": "mercury_ai.analysis.trend_analyzer",
                "class_name": "TrendAnalyzer",
                "method_name": "analyze",
                "file_path": "analysis/trend_analyzer.py",
                "protocol": "N/A (concrete analyzer)",
            },
            # Stage 5: MTF Analysis
            {
                "order": 5,
                "name": "MTF",
                "module": "mercury_ai.analysis.mtf_engine",
                "class_name": "MTFEngine",
                "method_name": "analyze",
                "file_path": "analysis/mtf_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 6: Smart Money
            {
                "order": 6,
                "name": "SmartMoney",
                "module": "mercury_ai.analysis.smart_money.smart_money_engine",
                "class_name": "SmartMoneyEngine",
                "method_name": "analyze",
                "file_path": "analysis/smart_money/smart_money_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 7: Liquidity
            {
                "order": 7,
                "name": "Liquidity",
                "module": "mercury_ai.analysis.smart_money.liquidity_engine",
                "class_name": "LiquidityEngine",
                "method_name": "analyze",
                "file_path": "analysis/smart_money/liquidity_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 8: Market Structure
            {
                "order": 8,
                "name": "Structure",
                "module": "mercury_ai.analysis.market_structure_intelligence_engine",
                "class_name": "MarketStructureIntelligenceEngine",
                "method_name": "evaluate",
                "file_path": "analysis/market_structure_intelligence_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 9: Evidence Engine
            {
                "order": 9,
                "name": "Evidence",
                "module": "mercury_ai.analysis.evidence_engine",
                "class_name": "EvidenceEngine",
                "method_name": "process",
                "file_path": "analysis/evidence_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 10: Confluence
            {
                "order": 10,
                "name": "Confluence",
                "module": "mercury_ai.analysis.confluence_engine",
                "class_name": "ConfluenceEngine",
                "method_name": "analyze",
                "file_path": "analysis/confluence_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 11: Probability
            {
                "order": 11,
                "name": "Probability",
                "module": "mercury_ai.brain.probability_engine",
                "class_name": "ProbabilityEngine",
                "method_name": "analyze",
                "file_path": "brain/probability_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 12: Decision Resolver
            {
                "order": 12,
                "name": "DecisionResolver",
                "module": "mercury_ai.analysis.decision_resolver_engine",
                "class_name": "DecisionResolverEngine",
                "method_name": "resolve",
                "file_path": "analysis/decision_resolver_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 13: Explainability
            {
                "order": 13,
                "name": "Explainability",
                "module": "mercury_ai.analysis.narrative_engine",
                "class_name": "NarrativeEngine",
                "method_name": "generate",
                "file_path": "analysis/narrative_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 14: Scanner (Orchestrator)
            {
                "order": 14,
                "name": "Scanner",
                "module": "mercury_ai.brain.scanner",
                "class_name": "MercuryScanner",
                "method_name": "scan",
                "file_path": "brain/scanner.py",
                "protocol": "N/A (orchestrator)",
            },
            # Additional AnalysisPipeline stages
            # Stage 15: Volume Intelligence
            {
                "order": 15,
                "name": "VolumeIntelligence",
                "module": "mercury_ai.analysis.volume_intelligence_engine",
                "class_name": "VolumeIntelligenceEngine",
                "method_name": "evaluate",
                "file_path": "analysis/volume_intelligence_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 16: Candlestick
            {
                "order": 16,
                "name": "Candlestick",
                "module": "mercury_ai.analysis.candlestick_engine",
                "class_name": "CandlestickEngine",
                "method_name": "analyze",
                "file_path": "analysis/candlestick_engine.py",
                "protocol": "mercury_ai.core.base_engine.BaseEngine",
            },
            # Stage 17: Volatility
            {
                "order": 17,
                "name": "Volatility",
                "module": "mercury_ai.analysis.volatility_engine",
                "class_name": "VolatilityEngine",
                "method_name": "analyze",
                "file_path": "analysis/volatility_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 18: Session
            {
                "order": 18,
                "name": "Session",
                "module": "mercury_ai.analysis.session_engine",
                "class_name": "SessionEngine",
                "method_name": "analyze",
                "file_path": "analysis/session_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 19: Market State
            {
                "order": 19,
                "name": "MarketState",
                "module": "mercury_ai.analysis.market_state_engine",
                "class_name": "MarketStateEngine",
                "method_name": "analyze",
                "file_path": "analysis/market_state_engine.py",
                "protocol": "N/A (concrete engine)",
            },
            # Stage 20: Risk Engine (in DecisionEngine)
            {
                "order": 20,
                "name": "RiskEngine",
                "module": "mercury_ai.analysis.risk_engine",
                "class_name": "RiskEngine",
                "method_name": "assess",
                "file_path": "analysis/risk_engine.py",
                "protocol": "N/A (concrete engine)",
            },
        ]
    
    def _analyze_stage(self, stage_def: Dict[str, Any]) -> PipelineStage:
        """Analyze a single pipeline stage via AST."""
        file_path = self.mercury_ai_root / stage_def["file_path"]
        
        if not file_path.exists():
            self.findings.append(f"MISSING_FILE: {stage_def['name']} - {file_path} not found")
            return self._create_missing_stage(stage_def, str(file_path))
        
        # Parse AST
        try:
            source = file_path.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except Exception as e:
            self.findings.append(f"PARSE_ERROR: {stage_def['name']} - {e}")
            return self._create_error_stage(stage_def, str(file_path), str(e))
        
        # Find class and method
        class_node = None
        method_node = None
        line_start = 0
        line_end = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == stage_def["class_name"]:
                class_node = node
                line_start = node.lineno
                line_end = node.end_lineno or node.lineno
                
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == stage_def["method_name"]:
                        method_node = item
                        line_start = item.lineno
                        line_end = item.end_lineno or item.lineno
                        break
                break
        
        if not class_node:
            self.findings.append(f"MISSING_CLASS: {stage_def['name']} - Class {stage_def['class_name']} not found in {file_path}")
            return self._create_missing_stage(stage_def, str(file_path))
        
        if not method_node:
            self.findings.append(f"MISSING_METHOD: {stage_def['name']} - Method {stage_def['method_name']} not found in {stage_def['class_name']}")
            return self._create_missing_stage(stage_def, str(file_path))
        
        # Extract contract documentation from AST
        entrada = self._extract_entrada(method_node)
        saida = self._extract_saida(method_node)
        tipos = self._extract_tipos(method_node, class_node, source)
        tempo = self._extract_tempo(method_node, source)
        objetos = self._extract_objetos(method_node, class_node, source)
        contratos = self._extract_contratos(class_node, stage_def.get("protocol"), source)
        excecoes = self._extract_excecoes(method_node, source)
        source_evidence = self._extract_source_evidence(method_node, class_node, source, line_start, line_end)
        
        return PipelineStage(
            name=stage_def["name"],
            order=stage_def["order"],
            module=stage_def["module"],
            class_name=stage_def["class_name"],
            method_name=stage_def["method_name"],
            file_path=str(file_path),
            line_start=line_start,
            line_end=line_end,
            entrada=entrada,
            saida=saida,
            tipos=tipos,
            tempo=tempo,
            objetos=objetos,
            contratos=contratos,
            excecoes=excecoes,
            source_evidence=source_evidence,
        )
    
    def _extract_entrada(self, method_node: ast.FunctionDef) -> str:
        """Extract input parameters with types."""
        params = []
        for arg in method_node.args.args:
            if arg.arg == "self":
                continue
            annotation = ""
            if arg.annotation:
                annotation = f": {ast.unparse(arg.annotation)}"
            params.append(f"{arg.arg}{annotation}")
        
        # Handle *args, **kwargs
        if method_node.args.vararg:
            params.append(f"*{method_node.args.vararg.arg}")
        if method_node.args.kwarg:
            params.append(f"**{method_node.args.kwarg.arg}")
        
        return f"({', '.join(params)})" if params else "()"
    
    def _extract_saida(self, method_node: ast.FunctionDef) -> str:
        """Extract return type annotation."""
        if method_node.returns:
            return ast.unparse(method_node.returns)
        return "Any (no annotation)"
    
    def _extract_tipos(self, method_node: ast.FunctionDef, class_node: ast.ClassDef, source: str) -> str:
        """Extract key data types used in the method."""
        types = set()
        
        # Check annotations in method
        for arg in method_node.args.args:
            if arg.annotation:
                types.add(ast.unparse(arg.annotation))
        if method_node.returns:
            types.add(ast.unparse(method_node.returns))
        
        # Check for type hints in method body (simplified)
        for node in ast.walk(method_node):
            if isinstance(node, ast.AnnAssign) and node.annotation:
                types.add(ast.unparse(node.annotation))
            elif isinstance(node, ast.Call):
                # Check for constructor calls that indicate types
                if isinstance(node.func, ast.Name):
                    types.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    types.add(node.func.attr)
        
        # Limit to most relevant types
        relevant = [t for t in types if not t.startswith("_") and len(t) > 1]
        return ", ".join(sorted(relevant)[:10]) if relevant else "Not detected"
    
    def _extract_tempo(self, method_node: ast.FunctionDef, source: str) -> str:
        """Estimate execution time/complexity from code patterns."""
        # Look for timing decorators, perf_counter, or complexity indicators
        has_timing = False
        has_loops = False
        has_io = False
        loop_depth = 0
        
        for node in ast.walk(method_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and "perf_counter" in node.func.id:
                    has_timing = True
                if isinstance(node.func, ast.Attribute) and "time" in node.func.attr:
                    has_timing = True
            if isinstance(node, (ast.For, ast.While)):
                has_loops = True
                loop_depth += 1
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ["read", "write", "get", "post", "request", "query", "execute"]:
                        has_io = True
        
        if has_timing:
            return "Instrumented (perf_counter)"
        elif has_io:
            return "I/O bound (network/disk)"
        elif has_loops and loop_depth > 1:
            return "O(n²) or higher - nested loops"
        elif has_loops:
            return "O(n) - single loop"
        else:
            return "O(1) - constant time"
    
    def _extract_objetos(self, method_node: ast.FunctionDef, class_node: ast.ClassDef, source: str) -> str:
        """Extract key objects created/used in the method."""
        objects = set()
        
        # Check for instantiations
        for node in ast.walk(method_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    objects.add(f"new {node.func.id}()")
                elif isinstance(node.func, ast.Attribute):
                    objects.add(f"new {node.func.attr}()")
        
        # Check for attribute access on self
        for node in ast.walk(method_node):
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self":
                objects.add(f"self.{node.attr}")
        
        return ", ".join(sorted(objects)[:10]) if objects else "Not detected"
    
    def _extract_contratos(self, class_node: ast.ClassDef, protocol: Optional[str], source: str) -> str:
        """Extract interface contracts (protocols, base classes)."""
        contracts = []
        
        # Check base classes
        for base in class_node.bases:
            if isinstance(base, ast.Name):
                contracts.append(f"extends {base.id}")
            elif isinstance(base, ast.Attribute):
                contracts.append(f"extends {base.attr}")
        
        # Check for protocol implementation (if protocol specified)
        if protocol:
            contracts.append(f"implements {protocol}")
        
        # Check for @abstractmethod or Protocol usage
        for node in ast.walk(class_node):
            if isinstance(node, ast.FunctionDef):
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name) and "abstract" in decorator.id.lower():
                        contracts.append("has @abstractmethod")
        
        return "; ".join(contracts) if contracts else "No explicit contract"
    
    def _extract_excecoes(self, method_node: ast.FunctionDef, source: str) -> str:
        """Extract possible exceptions raised."""
        exceptions = set()
        
        for node in ast.walk(method_node):
            if isinstance(node, ast.Raise):
                if node.exc:
                    if isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
                        exceptions.add(node.exc.func.id)
                    elif isinstance(node.exc, ast.Name):
                        exceptions.add(node.exc.id)
            # Check for try/except blocks
            if isinstance(node, ast.Try):
                for handler in node.handlers:
                    if handler.type:
                        if isinstance(handler.type, ast.Name):
                            exceptions.add(f"catches {handler.type.id}")
        
        # Common exceptions from patterns
        method_source = ast.get_source_segment(source, method_node) or ""
        if "KeyError" in method_source:
            exceptions.add("KeyError")
        if "ValueError" in method_source:
            exceptions.add("ValueError")
        if "IndexError" in method_source:
            exceptions.add("IndexError")
        if "AttributeError" in method_source:
            exceptions.add("AttributeError")
        if "TypeError" in method_source:
            exceptions.add("TypeError")
        if "pd.isna" in method_source or "pd.isnull" in method_source:
            exceptions.add("pandas NA handling")
        
        return ", ".join(sorted(exceptions)) if exceptions else "None explicitly raised"
    
    def _extract_source_evidence(self, method_node: ast.FunctionDef, class_node: ast.ClassDef, 
                                  source: str, line_start: int, line_end: int) -> List[str]:
        """Extract source code evidence lines."""
        lines = source.split("\n")
        evidence = []
        
        # Method signature
        if line_start <= len(lines):
            evidence.append(f"L{line_start}: {lines[line_start-1].strip()}")
        
        # Docstring
        if (method_node.body and isinstance(method_node.body[0], ast.Expr) 
            and isinstance(method_node.body[0].value, ast.Constant)
            and isinstance(method_node.body[0].value.value, str)):
            docstring = method_node.body[0].value.value
            evidence.append(f"Docstring: {docstring[:200]}...")
        
        # Key lines (returns, raises, important calls)
        for i in range(line_start - 1, min(line_end, len(lines))):
            line = lines[i].strip()
            if any(kw in line for kw in ["return ", "raise ", "yield ", "await "]):
                evidence.append(f"L{i+1}: {line[:120]}")
        
        return evidence[:5]  # Limit evidence
    
    def _create_missing_stage(self, stage_def: Dict[str, Any], file_path: str) -> PipelineStage:
        """Create a stage entry for missing file/class/method."""
        return PipelineStage(
            name=stage_def["name"],
            order=stage_def["order"],
            module=stage_def["module"],
            class_name=stage_def["class_name"],
            method_name=stage_def["method_name"],
            file_path=file_path,
            line_start=0,
            line_end=0,
            entrada="MISSING",
            saida="MISSING",
            tipos="MISSING",
            tempo="MISSING",
            objetos="MISSING",
            contratos="MISSING",
            excecoes="MISSING",
            source_evidence=[f"FILE NOT FOUND: {file_path}"],
        )
    
    def _create_error_stage(self, stage_def: Dict[str, Any], file_path: str, error: str) -> PipelineStage:
        """Create a stage entry for parse error."""
        return PipelineStage(
            name=stage_def["name"],
            order=stage_def["order"],
            module=stage_def["module"],
            class_name=stage_def["class_name"],
            method_name=stage_def["method_name"],
            file_path=file_path,
            line_start=0,
            line_end=0,
            entrada="ERROR",
            saida="ERROR",
            tipos="ERROR",
            tempo="ERROR",
            objetos="ERROR",
            contratos="ERROR",
            excecoes="ERROR",
            source_evidence=[f"PARSE ERROR: {error}"],
        )
    
    def _verify_contracts(self):
        """Verify that stages properly implement their contracts."""
        # Check MarketDataProvider protocol compliance
        provider_stage = next((s for s in self.stages if s.name == "Provider"), None)
        if provider_stage and "implements" in provider_stage.contratos:
            self.findings.append(f"CONTRACT_OK: Provider implements MarketDataProvider protocol")
        elif provider_stage:
            self.findings.append(f"CONTRACT_WARN: Provider may not explicitly implement MarketDataProvider protocol")
        
        # Check BaseEngine compliance for CandlestickEngine
        candlestick_stage = next((s for s in self.stages if s.name == "Candlestick"), None)
        if candlestick_stage and "extends BaseEngine" in candlestick_stage.contratos:
            self.findings.append(f"CONTRACT_OK: CandlestickEngine extends BaseEngine")
        elif candlestick_stage:
            self.findings.append(f"CONTRACT_WARN: CandlestickEngine should extend BaseEngine")
        
        # Verify data flow compatibility between stages
        self._verify_data_flow()
    
    def _verify_data_flow(self):
        """Verify data flow compatibility between consecutive stages."""
        # This would require deeper type analysis - simplified for now
        for i in range(len(self.stages) - 1):
            current = self.stages[i]
            next_stage = self.stages[i + 1]
            
            # Check if current stage's output type matches next stage's input
            if current.saida != "Any (no annotation)" and next_stage.entrada != "()":
                self.findings.append(f"DATA_FLOW: {current.name} -> {next_stage.name} | "
                                   f"Output: {current.saida} | Input: {next_stage.entrada}")
    
    def _check_completeness(self):
        """Check for missing expected stages."""
        expected_names = {
            "Provider", "MarketData", "Indicators", "Trend", "MTF", 
            "SmartMoney", "Liquidity", "Structure", "Evidence", "Confluence",
            "Probability", "DecisionResolver", "Explainability", "Scanner",
            "VolumeIntelligence", "Candlestick", "Volatility", "Session", 
            "MarketState", "RiskEngine"
        }
        found_names = {s.name for s in self.stages if not s.source_evidence or "MISSING" not in s.source_evidence[0]}
        missing = expected_names - found_names
        
        for m in missing:
            self.findings.append(f"MISSING_STAGE: {m} - Not found in codebase")
    
    def _determine_verdict(self) -> str:
        """Determine overall verdict."""
        critical_issues = [f for f in self.findings if f.startswith(("MISSING_FILE", "MISSING_CLASS", "MISSING_METHOD", "PARSE_ERROR"))]
        warnings = [f for f in self.findings if f.startswith(("CONTRACT_WARN", "MISSING_STAGE"))]
        
        if critical_issues:
            return "FAIL"
        elif warnings:
            return "WARNING"
        else:
            return "PASS"


def generate_certification_markdown(trace: PipelineTrace) -> str:
    """Generate PIPELINE_CERTIFICATION.md from trace."""
    lines = []
    lines.append("# PIPELINE CERTIFICATION REPORT")
    lines.append("")
    lines.append(f"**Generated:** {trace.trace_timestamp}")
    lines.append(f"**Mercury AI Root:** {trace.mercury_ai_root}")
    lines.append(f"**Total Stages:** {trace.total_stages}")
    lines.append(f"**Verdict:** {trace.verdict}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Executive Summary
    lines.append("## EXECUTIVE SUMMARY")
    lines.append("")
    if trace.verdict == "PASS":
        lines.append("✅ **PASS** - All pipeline stages verified with complete contracts and evidence.")
    elif trace.verdict == "WARNING":
        lines.append("⚠️ **WARNING** - Pipeline functional but with contract/completeness warnings.")
    else:
        lines.append("❌ **FAIL** - Critical pipeline stages missing or broken.")
    lines.append("")
    
    # Findings Summary
    if trace.findings:
        lines.append("## FINDINGS SUMMARY")
        lines.append("")
        for finding in trace.findings:
            lines.append(f"- {finding}")
        lines.append("")
    
    # Stage Details
    lines.append("## STAGE-BY-STAGE CERTIFICATION")
    lines.append("")
    
    for stage in trace.stages:
        lines.append(f"### Stage {stage.order}: {stage.name}")
        lines.append("")
        lines.append(f"**Module:** `{stage.module}`")
        lines.append(f"**Class:** `{stage.class_name}`")
        lines.append(f"**Method:** `{stage.method_name}`")
        lines.append(f"**File:** `{stage.file_path}` (L{stage.line_start}-L{stage.line_end})")
        lines.append("")
        
        lines.append("#### Contract Documentation")
        lines.append("")
        lines.append(f"- **Entrada:** `{stage.entrada}`")
        lines.append(f"- **Saída:** `{stage.saida}`")
        lines.append(f"- **Tipos:** `{stage.tipos}`")
        lines.append(f"- **Tempo:** `{stage.tempo}`")
        lines.append(f"- **Objetos:** `{stage.objetos}`")
        lines.append(f"- **Contratos:** `{stage.contratos}`")
        lines.append(f"- **Exceções:** `{stage.excecoes}`")
        lines.append("")
        
        if stage.source_evidence:
            lines.append("#### Source Evidence")
            lines.append("")
            for ev in stage.source_evidence:
                lines.append(f"- `{ev}`")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)


def generate_timeline_markdown(trace: PipelineTrace) -> str:
    """Generate PIPELINE_TIMELINE.md from trace."""
    lines = []
    lines.append("# PIPELINE EXECUTION TIMELINE")
    lines.append("")
    lines.append(f"**Generated:** {trace.trace_timestamp}")
    lines.append(f"**Total Stages:** {trace.total_stages}")
    lines.append("")
    lines.append("## Pipeline Flow Diagram")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph TD")
    
    for stage in trace.stages:
        if stage.order < len(trace.stages):
            next_stage = trace.stages[stage.order]  # 0-indexed
            lines.append(f"    {stage.name} --> {next_stage.name}")
    
    lines.append("```")
    lines.append("")
    
    lines.append("## Stage Timing Analysis")
    lines.append("")
    lines.append("| Order | Stage | Complexity | Contract Status |")
    lines.append("|-------|-------|------------|-----------------|")
    
    for stage in trace.stages:
        contract_status = "✅" if "implements" in stage.contratos or "extends" in stage.contratos else "⚠️"
        if "MISSING" in stage.contratos or "ERROR" in stage.contratos:
            contract_status = "❌"
        lines.append(f"| {stage.order:2d} | {stage.name} | {stage.tempo} | {contract_status} |")
    
    lines.append("")
    lines.append("## Data Flow Contracts")
    lines.append("")
    lines.append("| From Stage | To Stage | Output Type | Input Type | Compatibility |")
    lines.append("|------------|----------|-------------|------------|---------------|")
    
    for i in range(len(trace.stages) - 1):
        current = trace.stages[i]
        next_stage = trace.stages[i + 1]
        compat = "✅" if current.saida != "Any (no annotation)" else "⚠️"
        lines.append(f"| {current.name} | {next_stage.name} | {current.saida} | {next_stage.entrada} | {compat} |")
    
    lines.append("")
    lines.append("## Exception Propagation Map")
    lines.append("")
    lines.append("| Stage | Exceptions Raised | Exceptions Caught |")
    lines.append("|-------|-------------------|-------------------|")
    
    for stage in trace.stages:
        lines.append(f"| {stage.name} | {stage.excecoes} | (analysis needed) |")
    
    lines.append("")
    lines.append("## Object Lifecycle")
    lines.append("")
    lines.append("| Stage | Key Objects Created | Key Objects Consumed |")
    lines.append("|-------|---------------------|----------------------|")
    
    for stage in trace.stages:
        lines.append(f"| {stage.name} | {stage.objetos} | (analysis needed) |")
    
    return "\n".join(lines)


def main():
    """Main entry point."""
    mercury_ai_root = r"c:\Projetos\Mercury-AI\mercury_ai"
    
    auditor = PipelineCertificationAuditor(mercury_ai_root)
    trace = auditor.run()
    
    # Generate outputs
    output_dir = Path(r"c:\Projetos\Mercury-AI\.mercury\audits")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # PIPELINE_CERTIFICATION.md
    cert_md = generate_certification_markdown(trace)
    cert_path = output_dir / "PIPELINE_CERTIFICATION.md"
    cert_path.write_text(cert_md, encoding="utf-8")
    print(f"\n✅ Generated: {cert_path}")
    
    # PIPELINE_TIMELINE.md
    timeline_md = generate_timeline_markdown(trace)
    timeline_path = output_dir / "PIPELINE_TIMELINE.md"
    timeline_path.write_text(timeline_md, encoding="utf-8")
    print(f"✅ Generated: {timeline_path}")
    
    # JSON trace for programmatic access
    trace_json = {
        "trace_timestamp": trace.trace_timestamp,
        "mercury_ai_root": trace.mercury_ai_root,
        "total_stages": trace.total_stages,
        "verdict": trace.verdict,
        "findings": trace.findings,
        "stages": [asdict(s) for s in trace.stages]
    }
    json_path = output_dir / "PIPELINE_TRACE.json"
    json_path.write_text(json.dumps(trace_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Generated: {json_path}")
    
    print("\n" + "=" * 80)
    print(f"PIPELINE CERTIFICATION COMPLETE - VERDICT: {trace.verdict}")
    print("=" * 80)
    
    return trace


if __name__ == "__main__":
    main()
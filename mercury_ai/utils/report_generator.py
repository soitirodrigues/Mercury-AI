import json
import csv
import platform
import sys
import datetime
from typing import Any, Dict, List

class BenchmarkReportGenerator:
    def __init__(self, pipeline_name: str, config: Dict[str, Any]):
        self.pipeline_name = pipeline_name
        self.config = config
        self.metadata = {
            "hardware": platform.processor(),
            "os": platform.system(),
            "python_version": sys.version,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def generate_json(self, data: Dict[str, Any]) -> str:
        report = {"metadata": self.metadata, "config": self.config, "data": data}
        return json.dumps(report, indent=2)

    def generate_csv(self, metrics: List[Dict[str, Any]], filename: str):
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=metrics[0].keys())
            writer.writeheader()
            writer.writerows(metrics)

    def generate_markdown(self, data: Dict[str, Any]) -> str:
        lines = [f"# Benchmark Report: {self.pipeline_name}", ""]
        lines.append("## Metadata")
        for k, v in self.metadata.items():
            lines.append(f"- **{k.capitalize()}**: {v}")
        lines.append("")
        
        lines.append("## Summary")
        lines.append(f"Result: {json.dumps(data, indent=2)}")
        
        return "\n".join(lines)

    def generate_html(self, data: Dict[str, Any]) -> str:
        # Minimal HTML structure, designed for future expansion
        return f"<html><body><h1>Report: {self.pipeline_name}</h1><pre>{json.dumps(data, indent=2)}</pre></body></html>"

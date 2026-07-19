import json
import pandas as pd
import zipfile
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from mercury_ai.analysis.data_exporter import DataExporter

class ExportCenter:
    """
    Centro de exportação institucional aprimorado.
    """
    def __init__(self, export_dir: str = "exports"):
        self.exporter = DataExporter(export_dir=export_dir)
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)

    def export_data(self, 
                    data: List[Dict[str, Any]], 
                    name: str, 
                    formats: List[str], 
                    filter_func: Optional[Callable] = None,
                    partial: bool = False):
        
        # Apply filter if provided
        if filter_func:
            data = [item for item in data if filter_func(item)]
            
        # Apply partial/full
        if partial and len(data) > 10:
            data = data[:10]

        df = pd.DataFrame(data)
        
        for fmt in formats:
            path = self.export_dir / f"{name}.{fmt}"
            if fmt == 'json':
                with open(path, "w") as f:
                    json.dump(data, f, indent=4, default=str)
            elif fmt == 'csv':
                df.to_csv(path, index=False)
            elif fmt == 'xlsx':
                try:
                    df.to_excel(path, index=False)
                except Exception:
                    pass # Excel support not available
            elif fmt == 'zip':
                with zipfile.ZipFile(path, 'w') as zipf:
                    zipf.writestr(f"{name}.json", json.dumps(data, indent=4, default=str))
            elif fmt == 'pdf':
                # Basic PDF export using pandas to_string
                with open(path.with_suffix('.txt'), "w") as f:
                    f.write(df.to_string())

    def export_history(self, formats=['json', 'csv', 'xlsx', 'zip'], filter_func=None, partial=False):
        data = self.exporter.history.query()
        self.export_data(data, "history", formats, filter_func, partial)

    def export_snapshots(self, formats=['json', 'zip'], filter_func=None, partial=False):
        snapshots = self.exporter.snapshot_logger.list_snapshots()
        data = [self.exporter.snapshot_logger.load_snapshot(s) for s in snapshots]
        self.export_data(data, "snapshots", formats, filter_func, partial)

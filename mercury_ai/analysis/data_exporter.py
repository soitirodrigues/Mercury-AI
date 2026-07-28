import json
import pandas as pd
import zipfile
import logging
from pathlib import Path
from mercury_ai.analysis.operational_history import OperationalHistory
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
from mercury_ai.utils.atomic_io import atomic_json_write
from typing import Dict, Any, List

class DataExporter:
    """
    Camada de exportação de dados institucionais.
    """
    def __init__(self, export_dir: str = "exports"):
        self.history = OperationalHistory()
        self.snapshot_logger = DecisionSnapshotLogger()
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)
        
    def _export_to_formats(self, name: str, data: Any, formats: List[str]):
        df = None
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
            
        for fmt in formats:
            path = self.export_dir / f"{name}.{fmt}"
            if fmt == 'json':
                atomic_json_write(str(path), data, indent=4, default=str)
            elif fmt == 'csv' and df is not None:
                df.to_csv(path, index=False)
            elif fmt == 'xlsx' and df is not None:
                try:
                    df.to_excel(path, index=False)
                except ImportError:
                    logging.warning("Excel support not available for %s.", name)
            elif fmt == 'zip':
                with zipfile.ZipFile(path, 'w') as zipf:
                    zipf.writestr(f"{name}.json", json.dumps(data, indent=4, default=str))

    def export_history(self, formats=['json', 'csv', 'xlsx', 'zip']):
        data = self.history.query()
        self._export_to_formats("history", data, formats)
        
    def export_snapshots(self, formats=['json', 'zip']):
        snapshots = self.snapshot_logger.list_snapshots()
        data = [self.snapshot_logger.load_snapshot(s) for s in snapshots]
        self._export_to_formats("snapshots", data, formats)
        
    def export_all(self):
        self.export_history()
        self.export_snapshots()

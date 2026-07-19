import json
import os
from mercury_ai.config import settings

class MercuryConfigCenter:
    """
    Central de persistência de configurações do sistema.
    """
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        # Minimal defaults to ensure structure exists
        self.settings = {
            "PROVIDERS": {},
            "SCANNER": {},
            "DASHBOARD": {},
            "REPLAY": {},
            "DEMO": {},
            "ASSET_REGISTRY": {},
            "BROKER_PROFILE": {},
            "SNAPSHOTS": {},
            "LOGS": {},
            "GENERAL": {"read_only": settings.READ_ONLY}
        }
        self._load_from_file()

    def _load_from_file(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                try:
                    loaded = json.load(f)
                    for category, category_settings in loaded.items():
                        if category in self.settings:
                            self.settings[category].update(category_settings)
                        else:
                            self.settings[category] = category_settings
                except json.JSONDecodeError:
                    pass

    def save(self, category: str, new_settings: dict):
        if category in self.settings:
            self.settings[category].update(new_settings)
        else:
            self.settings[category] = new_settings
        with open(self.config_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get(self, category: str, key: str = None, default=None):
        if category not in self.settings:
            return default
        if key:
            return self.settings[category].get(key, default)
        return self.settings[category]

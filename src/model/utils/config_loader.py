import yaml
from typing import Any, Dict


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError("Config file must contain a dictionary at the top level")
        return data
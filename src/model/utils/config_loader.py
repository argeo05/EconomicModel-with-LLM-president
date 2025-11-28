import yaml
from typing import Any, Dict


def load_config(path: str) -> Dict[str, Any]:
    """Load configuration from YAML file.

    Args:
        path: Path to YAML config file

    Returns:
        Configuration dictionary

    Raises:
        ValueError: If config file doesn't contain a dictionary
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError("Config file must contain a dictionary at the top level")
        return data
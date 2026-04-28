import os
import sys

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("Please install tomli to parse the settings file in python < 3.11")
        sys.exit(1)


def load_config(config_path: str = "settings.toml") -> dict:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, "rb") as f:
        config = tomllib.load(f)
    
    return config

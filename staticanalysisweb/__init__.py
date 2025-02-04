from pathlib import Path
import tomllib

config_path = Path('setup.toml')
try:
    with open(config_path, 'rb') as f:
        CONFIG = tomllib.load(f)
except FileNotFoundError:
    print("Failed to load toml config file.")
    print(f"Expected path is {config_path.resolve()}")
    exit
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    tech_lib: str = os.environ.get("TECH_LIB", "pandas_ta")  # or 'talib'
    seed: int = int(os.environ.get("SEED", "42"))

SETTINGS = Settings()

import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks" 
SRC_DIR = PROJECT_ROOT / "src"
UTILITIES_DIR = PROJECT_ROOT / "utilities"
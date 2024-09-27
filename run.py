import sys
from pathlib import Path
from src.app.main import create_app as backend_app

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))


app = backend_app()
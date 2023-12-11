import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from src.app.main import create_app as backend_app

# Za руtноп

app = backend_app()

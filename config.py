from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

APPDIR = Path(os.path.dirname(os.path.realpath(__file__)))

LOCAL_FOLDER = APPDIR / '.local'
LOCAL_FOLDER.mkdir(exist_ok=True)

DBPATH = APPDIR / '.local/pericias.fdb'
DB_USER= os.getenv("DB_USER", "")
DB_PASSWORD= os.getenv("DB_PASSWORD", "")
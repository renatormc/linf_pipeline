from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

if os.name == "nt":
    os.environ['PATH'] = f"{os.environ['PATH']};{os.getenv('POSTGRES_BIN')}"
    os.environ['PATH'] = f"{os.environ['PATH']};{os.getenv('FIREBIRD_BIN')}"

APPDIR = Path(os.path.dirname(os.path.realpath(__file__)))

LOCAL_FOLDER = APPDIR / '.local'
LOCAL_FOLDER.mkdir(exist_ok=True)

DBPATH = APPDIR / '.local/pericias.fdb'
DBPATH_BACKUP = APPDIR / '.local/pericias_backup.fbk'
DB_USER= os.getenv("DB_USER", "")
DB_PASSWORD= os.getenv("DB_PASSWORD", "")

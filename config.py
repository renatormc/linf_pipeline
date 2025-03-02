from pathlib import Path
import os

APPDIR = Path(os.path.dirname(os.path.realpath(__file__)))

LOCAL_FOLDER = APPDIR / 'local'
LOCAL_FOLDER.mkdir(exist_ok=True)
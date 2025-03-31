from pathlib import Path
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

def compile_ui(filename: str) -> None:
    print(f"Compiling {filename}")
    path = Path(filename)
    to_path = path.parent / f"{path.stem}_ui.py"
    subprocess.run(["uv", "run", "pyside6-uic", str(path), "-o", str(to_path)])

class UIFileChangeHandler(FileSystemEventHandler):
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".ui"):
            compile_ui(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".ui"):
            compile_ui(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".ui"):
            path = Path(event.src_path)
            to_path = path.parent / f"{path.stem}_ui.py"
            try:
                to_path.unlink()
            except FileNotFoundError:
                pass

def watch_folder(folder_path):
    event_handler = UIFileChangeHandler(folder_path)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_to_watch = "."
    if os.path.isdir(folder_to_watch):
        print(f"Watching for changes in {folder_to_watch}...")
        watch_folder(folder_to_watch)
    else:
        print(f"The folder {folder_to_watch} does not exist.")

import os
from pathlib import Path
import subprocess
import config
import tempfile

from models import DBSession
from repo import clear_db

docker = False if os.name == "nt" else True

def exec_pg_cmd(args: list[str], **kwargs) -> None:
    if docker:
        subprocess.check_call(['docker', 'exec', '--env', f'PGPASSWORD={config.DB_PASSWORD}', 'postgres_pipeline'] + args, **kwargs)
        return
    env = os.environ.copy() 
    env["PGPASSWORD"] = config.DB_PASSWORD
    subprocess.run(args, env=env, **kwargs)


def backup_db() -> None:
    path = config.APPDIR / ".local/backup.tar"
    with path.open("w") as f:
        exec_pg_cmd(['pg_dump', '-d', 'pipeline', '-U', config.DB_USER, '-p', '5432', '-h', 'localhost', '-O', '-x', '-Ft'], stdout=f)
       
        
def restore_db() -> None:
    # exec_pg_cmd(['dropdb', '-U', config.DB_USER, '-p', '5432', '-h', 'localhost', 'pipeline'])
    # exec_pg_cmd(['createdb', '-U', config.DB_USER, '-p', '5432', '-h', 'localhost', 'pipeline'])
    with DBSession() as db_session:
        clear_db(db_session)
    path = '/app/.local/backup.tar' if docker else str(config.APPDIR / ".local/backup.tar")
    exec_pg_cmd(['pg_restore', '-U', config.DB_USER, '-p', '5432', '-h', 'localhost', '-d', 'pipeline', '-Ft', path])
    
    
    
def create_postgres_db() -> None:
    exec_pg_cmd(['dropdb', '--if-exists', '-U', config.DB_USER, '-p', '5432', '-h', 'localhost', 'pipeline'])
    exec_pg_cmd(['createdb', '-U', config.DB_USER, '-p', '5432', '-h', 'localhost', 'pipeline'])

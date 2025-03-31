import os
from pathlib import Path
import shutil
import subprocess
import config
import tempfile


docker = False if os.name == "nt" else True

def exec_pg_cmd(args: list[str], **kwargs) -> None:
    if docker:
        subprocess.check_call(['docker', 'exec', '--env', f'PGPASSWORD={config.DB_PASSWORD}', 'postgres_pipeline'] + args, **kwargs)
        return
    env = os.environ.copy() 
    env["PGPASSWORD"] = config.DB_PASSWORD
    subprocess.run(args, env=env, **kwargs)


def backup_db() -> None:
    # shutil.copy(config.DBPATH, config.DBPATH_BACKUP)
    path = config.APPDIR / ".local/backup.tar"
    with path.open("w") as f:
        exec_pg_cmd(['pg_dump', '-d', 'pipeline', '-U', config.DB_USER, '-p', '5432', '-h', 'localhost', '-O', '-x', '-Ft'], stdout=f)
    # subprocess.check_call(['gbak', '-b', '-user', 'SYSDBA', '-password', 'masterkey', str(config.DBPATH), str(config.DBPATH_BACKUP)])
        
def restore_db() -> None:
    exec_pg_cmd(['dropdb', '-U', config.DB_USER, '-p', '5432', '-h', 'localhost', 'pipeline'])
    exec_pg_cmd(['createdb', '-U', config.DB_USER, '-p', '5432', '-h', 'localhost', 'pipeline'])
    path = '/app/.local/backup.tar' if docker else str(config.APPDIR / ".local/backup.tar")
    exec_pg_cmd(['pg_restore', '-U', config.DB_USER, '-p', '5432', '-h', 'localhost', '-d', 'pipeline', '-Ft', path])
    # subprocess.check_call(['gbak', '-c', '-REP', '-user', 'SYSDBA', '-password', 'masterkey', str(config.DBPATH_BACKUP), str(config.DBPATH)])
    # try:
    #     config.DBPATH.unlink()
    # except FileNotFoundError:
    #     pass
    # shutil.copy(config.DBPATH_BACKUP, config.DBPATH)
    
    
def create_postgres_db() -> None:
    exec_pg_cmd(['dropdb', '--if-exists', '-U', config.DB_USER, '-p', '5432', '-h', 'localhost', 'pipeline'])
    exec_pg_cmd(['createdb', '-U', config.DB_USER, '-p', '5432', '-h', 'localhost', 'pipeline'])


# def create_firebird_db() -> None:
#     try:
#         config.DBPATH.unlink()
#     except FileNotFoundError:
#         pass
#     sql = f"CREATE DATABASE '{config.DBPATH}' USER 'SYSDBA' PASSWORD 'masterkey' PAGE_SIZE 8192 DEFAULT CHARACTER SET UTF8;"
#     script = Path(tempfile.gettempdir()) / "create.sql"
#     script.write_text(sql)
#     print(sql)
#     subprocess.check_call(["isql", "-user", "SYSDBA", "-password", "masterkey", "127.0.0.1:3050", "-i", str(script)])
#     from models import create_tables
#     create_tables()
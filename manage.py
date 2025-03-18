from pathlib import Path
import subprocess
import config
import tempfile

def backup_db() -> None:
    path = config.APPDIR / ".local/backup.tar"
    with path.open("w") as f:
        subprocess.run(['docker', 'exec', '--env', 'PGPASSWORD=pipeline', 'postgres_pipeline', 
                        'pg_dump', '-d', 'pipeline', '-U', 'pipeline', '-p', '5432', '-h', 'localhost', '-O', '-x', '-Ft'], stdout=f)
        
def restore_db() -> None:
    subprocess.run(['docker', 'exec', '--env', 'PGPASSWORD=pipeline', 'postgres_pipeline', 'dropdb', '-U', 'pipeline', '-p', '5432', '-h', 'localhost', 'pipeline'])
    subprocess.run(['docker', 'exec','--env', 'PGPASSWORD=pipeline', 'postgres_pipeline', 'createdb', '-U', 'pipeline', '-p', '5432', '-h', 'localhost', 'pipeline'])
    subprocess.run(['docker', 'exec', '--env', 'PGPASSWORD=pipeline','postgres_pipeline', 'pg_restore', '-U', 'pipeline', '-p', '5432', '-h', 'localhost', '-d', 'pipeline', '-Ft', '/app/.local/backup.tar'])
    
def create_firebird_db() -> None:
    isql = r'C:\Program Files\Firebird\Firebird_4_0\isql.exe'
    text = f"CREATE DATABASE '{config.DBPATH}' USER 'SYSDBA' PASSWORD 'masterkey' PAGE_SIZE 8192 DEFAULT CHARACTER SET UTF8;"
    script = Path(tempfile.gettempdir()) / "create.sql"
    script.write_text(text)
    subprocess.check_call([str(isql), "-user", "SYSDBA", "-password", "masterkey", "127.0.0.1:3050", "-i", str(script)])
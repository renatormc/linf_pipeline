import subprocess
import config


def backup_db() -> None:
    path = config.APPDIR / ".local/backup.tar"
    with path.open("w") as f:
        subprocess.run(['docker', 'exec', '--env', 'PGPASSWORD=pipeline', 'postgres_pipeline', 
                        'pg_dump', '-d', 'pipeline', '-U', 'pipeline', '-p', '5432', '-h', 'localhost', '-O', '-x', '-Ft'], stdout=f)
        
def restore_db() -> None:
    subprocess.run(['docker', 'exec', '--env', 'PGPASSWORD=pipeline', 'postgres_pipeline', 'dropdb', '-U', 'pipeline', '-p', '5432', '-h', 'localhost', 'pipeline'])
    subprocess.run(['docker', 'exec','--env', 'PGPASSWORD=pipeline', 'postgres_pipeline', 'createdb', '-U', 'pipeline', '-p', '5432', '-h', 'localhost', 'pipeline'])
    subprocess.run(['docker', 'exec', '--env', 'PGPASSWORD=pipeline','postgres_pipeline', 'pg_restore', '-U', 'pipeline', '-p', '5432', '-h', 'localhost', '-d', 'pipeline', '-Ft', '/app/.local/backup.tar'])
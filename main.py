from typing import Literal
import click
from manage import create_postgres_db
import signal


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


@cli.command("simulate")
@click.option('--restore',  is_flag=True, show_default=True, default=False, help="Restore database.")
def simulate(restore: bool) -> None:
    if restore:
        from manage import restore_db
        restore_db()
    import sys
    from PySide6.QtWidgets import QApplication
    from gui.gui import SimulatorWindow
    app = QApplication(sys.argv)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    window = SimulatorWindow()
    window.show()
    sys.exit(app.exec())

    
    
@cli.command("backup")
def backup() -> None:
    from manage import backup_db
    backup_db()
    
    
@cli.command("restore")
def restore() -> None:
    from manage import restore_db
    restore_db()
    
   
    
@cli.command("createdb")
@click.argument("number", type=int)
def createdb(number: int) -> None:
    from pericia_generator import populate_db_cases
    from manage import backup_db
    from models import create_tables
    create_postgres_db()
    create_tables()
    print("Populating database")
    populate_db_cases(number)
    print("backup database")
    backup_db()


  
    

if __name__ == '__main__':
    cli(obj={})

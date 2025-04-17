from typing import Literal
import click
from manage import create_postgres_db
from simulation import print_stats


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.ensure_object(dict)

@cli.command("simulate")
@click.argument('type', type=click.Choice(['pipeline', 'current']))
def simulate(type: Literal['pipeline', 'current']) -> None:
    from simulation import simulate_lab
    simulate_lab(type)
    
    
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


@cli.command("stats")
def stats() -> None:
    print_stats()
    
    

if __name__ == '__main__':
    cli(obj={})

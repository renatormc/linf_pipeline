from typing import Literal
import click
from manage import create_postgres_db


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


@cli.command("gen-cases")
@click.argument("number", type=int)
def gen_cases(number: int) -> None:
    from pericia_generator import populate_db_cases
    from manage import backup_db
    print("Creating database")
    create_postgres_db()
    print("Populating database")
    populate_db_cases(number)
    print("backup database")
    backup_db()


@cli.command("simulate")
@click.argument('type', type=click.Choice(['pipeline', 'current']))
def simulate(type: Literal['pipeline', 'current']) -> None:
    from pericia_generator import populate_db_cases
    from simulation import simulate_lab
    from manage import restore_db
    restore_db()
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
def createdb() -> None:
    # create_firebird_db()
    create_postgres_db()


if __name__ == '__main__':
    cli(obj={})

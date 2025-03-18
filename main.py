import click
from manage import create_postgres_db


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


@cli.command("gen-cases")
def gen_cases() -> None:
    from pericia_generator import populate_db_cases
    populate_db_cases(500)


@cli.command("simulate")
def simulate() -> None:
    from pericia_generator import populate_db_cases
    from simulation import simulate_lab
    populate_db_cases(3000)
    simulate_lab()
    
    
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

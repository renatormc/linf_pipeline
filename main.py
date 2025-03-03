from datetime import datetime
import click

from pericia_generator import popular_db_pericias
from simulation import interval_iterator


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


@cli.command("gerar-pericias")
def gerar_pericias() -> None:
    popular_db_pericias(500)


@cli.command("simulate")
def simulate() -> None:
    for t in interval_iterator(datetime(2025, 3, 2, 0, 0, 0), datetime(2025, 3, 2, 23, 59, 59)):
        print(t)


if __name__ == '__main__':
    cli(obj={})

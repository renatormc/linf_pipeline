import click
from simulation import simular_atual, simular_pipeline
from pericia_generator import popular_db_pericias
import log

@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


@cli.command("gerar-pericias")
def gerar_pericias() -> None:
    popular_db_pericias(500)


@cli.command("simular")
def simulate() -> None:
    # simular_atual()
    popular_db_pericias(500)
    simular_pipeline()


if __name__ == '__main__':
    cli(obj={})

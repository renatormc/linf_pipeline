import click
from simulation import simular_atual, simular_pipeline
from pericia_generator import populate_db_cases
import log

@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


@cli.command("gen-cases")
def gen_cases() -> None:
    populate_db_cases(500)


@cli.command("simulate")
def simulate() -> None:
    # simular_atual()
    populate_db_cases(3000)
    simular_pipeline()


if __name__ == '__main__':
    cli(obj={})

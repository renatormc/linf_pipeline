import click

from pericia_generator import popular_db_pericias


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


@cli.command("gerar-pericias")
def gerar_pericias() -> None:
    popular_db_pericias(500)


if __name__ == '__main__':
    cli(obj={})

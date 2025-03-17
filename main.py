import click


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
    from simulation import simular_pipeline
    populate_db_cases(3000)
    simular_pipeline()
    
    
@cli.command("backup")
def backup() -> None:
    from manage import backup_db
    backup_db()
    
@cli.command("restore")
def restore() -> None:
    from manage import restore_db
    restore_db()


if __name__ == '__main__':
    cli(obj={})

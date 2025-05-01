import click


@click.group()
def main_cli() -> None:
    """Virtual Barcodes CLI"""
    pass


@main_cli.command()
def test_cli() -> None:
    """Test CLI command"""
    click.echo("CLI is working!")


def cli() -> None:
    """Entry point for the CLI"""
    main_cli()

import click

from barcodes.minter import mint_barcodes
from barcodes.store import add_barcodes_to_sheet, determine_new_barcodes, get_sheet


@click.group()
def main_cli() -> None:
    """Virtual Barcodes CLI"""
    pass


@main_cli.command()
def test_cli() -> None:
    """Test CLI command"""
    click.echo("CLI is working!")


@main_cli.command()
@click.argument("unit_code", type=str, required=True)
@click.argument("batch_size", type=int, required=True)
def mint(unit_code: str, batch_size: int) -> None:
    """
    Mint barcodes for a given unit code and batch size.

    Args:
        unit_code (str): The unit/division's code using the barcodes.
        batch_size (int): The number of barcodes to mint.
    """
    # Get the Google Sheet
    sh = get_sheet()
    barcodes = determine_new_barcodes(sh, batch_size)
    add_barcodes_to_sheet(barcodes, unit_code, sh)
    click.echo(f"Minted {len(barcodes)} barcodes for unit code {unit_code}.")


def cli() -> None:
    """Entry point for the CLI"""
    main_cli()

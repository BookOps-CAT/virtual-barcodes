from typing import Generator

from barcodes.barcode import VirtualBarcode


def mint_barcodes(
    starting_sequence: int, batch_size: int, prefix: int = 33633
) -> Generator[str, None, None]:
    """
    Mint a batch of 14-digit barcodes.

    Args:
        prefix (str): The prefix for the barcodes.
        starting_sequence (int): The starting number for the barcodes.
        batch_size (int): The number of barcodes to mint.

    Returns:
        list[str]: A list of minted barcodes.
    """
    for i in range(starting_sequence, starting_sequence + batch_size):
        barcode = VirtualBarcode(identifier=i, prefix=prefix)
        yield str(barcode)


def determine_starting_sequence(last_barcode: str) -> int:
    """Determine the starting sequence for minting barcodes.

    Args:
        last_barcode (str): The last barcode in the list.

    Returns:
        int: The starting sequence for minting barcodes.
    """
    if not last_barcode:
        return 1
    return int(last_barcode[5:-1]) + 1

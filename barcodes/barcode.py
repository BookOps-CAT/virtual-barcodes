# -*- coding: utf-8 -*-

from typing import Generator


class VirtualBarcode:
    def __init__(self, identifier: int, prefix: int = 33633):
        """
        Initialize the VirtualBarcode instance.

        Args:
            prefix (int): The prefix for the barcodes.
            identifier (int): The starting number for the barcodes without
                a prefix or digit check.
        """
        self.prefix = prefix
        self.zfill_identifier = str(identifier).zfill(8)
        self.digit_check: int = self._calculate_digit_check()

    def _calculate_digit_check(self) -> int:
        """
        Calculate the digit check for the barcode.
        The digit check is the last digit of the barcode, calculated using a
        specific algorithm defined in Sierra documentation.
        """
        digits = [int(d) for d in f"{self.prefix}{self.zfill_identifier}"]
        even_sum = sum(digits[i] for i in range(1, len(digits), 2))
        odd_digits = [digits[i] for i in range(0, len(digits), 2)]

        def get_odd_sum(i: int) -> int:
            i_doubled = i * 2
            if i_doubled > 9:
                return 1 + (i_doubled % 10)
            else:
                return i_doubled

        odd_sum = sum([get_odd_sum(i) for i in odd_digits])

        return (10 - ((even_sum + odd_sum) % 10)) % 10

    def __repr__(self):
        return f"{self.prefix}{self.zfill_identifier}{self.digit_check}"


def minter(
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

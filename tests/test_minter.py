from typing import Generator

import pytest

from barcodes.minter import mint_barcodes, determine_starting_sequence


def test_minter_return_type():
    assert isinstance(mint_barcodes(1, 73433), Generator)


def test_minter_return_value():
    minted_barcodes = []
    for barcode in mint_barcodes(1, 5, 73433):
        minted_barcodes.append(barcode)

    assert minted_barcodes == [
        "73433000000013",
        "73433000000021",
        "73433000000039",
        "73433000000047",
        "73433000000054",
    ]


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("", 1),
        ("12345000000019", 2),
        ("12345000000129", 13),
    ],
)
def test_determine_starting_sequence(arg, expectation):
    assert determine_starting_sequence(arg) == expectation

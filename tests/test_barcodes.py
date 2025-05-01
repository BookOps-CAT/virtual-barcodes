from typing import Generator

import pytest

from barcodes.barcode import VirtualBarcode, minter


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (1, 3),
        ("1", 3),
        ("00000001", 3),
        (2, 1),
        (12345678, 7),
        (99999999, 3),
        (23445571, 0),
    ],
)
def test_calculate_digit_check(arg, expectation):
    assert VirtualBarcode(prefix=73433, identifier=arg).digit_check == expectation


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (1, "73433000000013"),
        ("00000001", "73433000000013"),
        (12345678, "73433123456787"),
        (
            99999999,
            "73433999999993",
        ),
    ],
)
def test_VirtualBarcode_repr(arg, expectation):
    assert repr(VirtualBarcode(prefix=73433, identifier=arg)) == expectation


def test_VirtualBarcode_instance():
    barcode = VirtualBarcode(prefix=73433, identifier=1)
    assert barcode.prefix == 73433
    assert barcode.zfill_identifier == "00000001"
    assert barcode.digit_check == 3


def test_minter_return_type():
    assert isinstance(minter(1, 73433), Generator)


def test_minter_return_value():
    minted_barcodes = []
    for barcode in minter(1, 5, 73433):
        minted_barcodes.append(barcode)

    assert minted_barcodes == [
        "73433000000013",
        "73433000000021",
        "73433000000039",
        "73433000000047",
        "73433000000054",
    ]

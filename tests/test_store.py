from contextlib import nullcontext as does_not_raise

import pytest
import gspread


from barcodes.store import (
    # get_last_barcode,
    get_sheet,
    get_worksheet_by_name,
    prep_values_for_main_ws_update,
    prep_values_for_unit_ws_update,
)


# @pytest.mark.webtest
# def test_get_last_barcode(test_sheet_id):
#     gc = gspread.
#     with does_not_raise():
#         last_barcode = get_last_barcode(test_sheet_id)
#     assert isinstance(last_barcode, str)
#     assert len(last_barcode) == 14


@pytest.mark.webtest
def test_get_sheet(test_sheet_id):
    with does_not_raise():
        sh = get_sheet(test_sheet_id)
    assert isinstance(sh, gspread.spreadsheet.Spreadsheet)
    assert sh.id == test_sheet_id


@pytest.mark.webtest
def test_get_worksheet_by_name(test_sheet_id):
    with does_not_raise():
        sh = get_sheet(test_sheet_id)
        ws = get_worksheet_by_name("barcodes-to-date", sh)
    assert isinstance(ws, gspread.worksheet.Worksheet)
    assert ws.title == "barcodes-to-date"


@pytest.mark.webtest
def test_get_worksheet_by_name_not_found(test_sheet_id):
    with pytest.raises(gspread.WorksheetNotFound):
        sh = get_sheet(test_sheet_id)
        get_worksheet_by_name("non-existent-worksheet", sh)


def test_prep_values_for_main_ws_update():
    barcodes = ["12345678900013", "12345678900014"]
    unit_code = "DEV"
    assert prep_values_for_main_ws_update(barcodes, unit_code) == [
        ("12345678900013", "DEV"),
        ("12345678900014", "DEV"),
    ]


def test_prep_values_for_unit_ws_update():
    barcodes = ["12345678900013", "12345678900014"]
    assert prep_values_for_unit_ws_update(barcodes) == [
        ("12345678900013",),
        ("12345678900014",),
    ]


# def test_temp(test_sheet_id):
#     # from barcodes.store import create_worksheet
#     from barcodes.store import add_barcodes_to_sheet

#     barcodes = ["123456789015", "123456789016"]
#     add_barcodes_to_sheet(barcodes, "DEV", test_sheet_id)

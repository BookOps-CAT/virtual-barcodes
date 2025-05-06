from contextlib import nullcontext as does_not_raise

import pytest
import gspread


from barcodes.store import (
    add_barcodes_to_sheet,
    add_barcodes_to_worksheet,
    determine_new_barcodes,
    get_last_barcode,
    get_sheet,
    get_worksheet_by_name,
    prep_values_for_main_ws_update,
    prep_values_for_unit_ws_update,
)


@pytest.mark.webtest
def test_add_barcodes_to_main_worksheet(test_sheet):
    barcodes = [("12345678900013"), ("12345678900014")]
    main_ws = test_sheet.worksheet("barcodes-to-date")
    range_str = "A1:B2"
    values = prep_values_for_main_ws_update(barcodes, "TEST")
    with does_not_raise():
        add_barcodes_to_worksheet(range_str, values, main_ws)

    assert main_ws.get_all_values() == [
        ["12345678900013", "TEST"],
        ["12345678900014", "TEST"],
    ]


@pytest.mark.webtest
def test_add_barcodes_to_sheet(test_sheet):
    with does_not_raise():
        add_barcodes_to_sheet(
            ["12345678900013", "12345678900014"], "TEST-2", test_sheet
        )
    # tear down
    unit_ws = test_sheet.worksheet("TEST-2")
    main_ws = test_sheet.worksheet("barcodes-to-date")
    main_ws.delete_rows(2, 3)
    test_sheet.del_worksheet(unit_ws)


@pytest.mark.webtest
def test_determine_new_barcodes(test_sheet):
    # Add a barcode to the sheet for testing
    main_ws = test_sheet.worksheet("barcodes-to-date")
    main_ws.append_row(["33633000000019"])
    main_ws.append_row(["33633000000029"])

    new_barcodes = determine_new_barcodes(test_sheet, 5)
    assert new_barcodes == [
        "33633000000033",
        "33633000000041",
        "33633000000058",
        "33633000000066",
        "33633000000074",
    ]


@pytest.mark.webtest
def test_get_last_barcode_empty_sheet(test_sheet):
    last_barcode = get_last_barcode(test_sheet)
    assert last_barcode == ""


@pytest.mark.webtest
def test_get_last_barcode_with_data(test_sheet):
    # Add a barcode to the sheet for testing
    main_ws = test_sheet.worksheet("barcodes-to-date")
    main_ws.append_row(["12345678900013"])
    main_ws.append_row(["12345678900014"])

    last_barcode = get_last_barcode(test_sheet)
    assert last_barcode == "12345678900014"


@pytest.mark.webtest
def test_get_sheet(test_sheet_id):
    sh = get_sheet(test_sheet_id)
    assert isinstance(sh, gspread.spreadsheet.Spreadsheet)
    assert sh.id == test_sheet_id


@pytest.mark.webtest
def test_get_worksheet_by_name(test_sheet_id):
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

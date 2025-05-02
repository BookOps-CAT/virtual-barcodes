from contextlib import nullcontext as does_not_raise

import pytest
import gspread


from barcodes.store import get_sheet, get_worksheet_by_name


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


import json
from pathlib import Path
from typing import Any

import gspread
import pytest


@pytest.fixture
def test_sheet_id() -> Any:
    """Fixture to get the test Google Sheet ID."""
    fh = Path.home() / ".cred/.gsheet/dev-virtual-barcodes-sheet-id.json"
    with open(fh) as f:
        data = json.load(f)
    return data["key"]


@pytest.fixture
def test_sheet(test_sheet_id) -> gspread.spreadsheet.Spreadsheet:
    """Fixture to get the test Google Sheet."""
    cred_fh = Path.home() / ".cred/.gsheet/google-sheet-virtual-barcodes.json"
    gc = gspread.oauth(credentials_filename=cred_fh)
    sh = gc.open_by_key(test_sheet_id)
    return sh

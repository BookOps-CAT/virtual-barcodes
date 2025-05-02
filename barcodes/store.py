import os
import json
from pathlib import Path
from typing import Optional, Any

import gspread


def get_creds() -> Path:
    """Get the credentials for Google Sheets API."""
    fh = Path.home() / ".cred/.gsheet/google-sheet-virtual-barcodes.json"
    return fh


def get_default_sheet() -> Any:
    """Get the default virtual barcodes Google Sheet ID."""
    sheet_id_fh = Path.home() / ".cred/.gsheet/default-virtual-barcodes-sheet-id.json"
    with open(sheet_id_fh) as f:
        data = json.load(f)
    return data["key"]


def get_sheet(key: str = "") -> gspread.spreadsheet.Spreadsheet:
    """Get the virtual barcodes Google Sheet as gspread Spreadsheet object."""
    cred_fh = get_creds()
    gc = gspread.oauth(credentials_filename=cred_fh)

    if not key:
        key = get_default_sheet()
    sh = gc.open_by_key(key)
    return sh


def get_worksheet_by_name(
    name: str, sheet: gspread.spreadsheet.Spreadsheet
) -> gspread.worksheet.Worksheet:
    """Get a worksheet by name."""
    return sheet.worksheet(name)


def create_worksheet(
    name: str, sheet: gspread.spreadsheet.Spreadsheet, rows: int
) -> gspread.worksheet.Worksheet:
    """Create a new worksheet."""
    return sheet.add_worksheet(title=name, rows=rows, cols="5")

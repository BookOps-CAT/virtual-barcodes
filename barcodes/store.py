import json
from pathlib import Path
from typing import Any, Union

import gspread

from barcodes.minter import determine_starting_sequence, mint_barcodes


def add_barcodes_to_sheet(
    barcodes: list[str], unit_code: str, sh: gspread.spreadsheet.Spreadsheet
) -> None:
    """Add barcodes to the Google Sheet.

    Args:
        barcodes (list[str]): List of barcodes to add.
        unit_code (str): Unit/Division's code using the barcodes.
        sh (gspread.spreadsheet.Spreadsheet): gspread Spreadsheet instance.
    """
    try:
        unit_ws = get_worksheet_by_name(unit_code, sh)
    except gspread.WorksheetNotFound:
        unit_ws = create_worksheet(unit_code, sh, len(barcodes))

    # populate barcodes-to-date worksheet (main)
    main_ws = get_worksheet_by_name("barcodes-to-date", sh)
    main_range_str = calculate_range(barcodes, main_ws)
    main_values = prep_values_for_main_ws_update(barcodes, unit_code)
    main_ws.add_rows(len(barcodes))
    add_barcodes_to_worksheet(main_range_str, main_values, main_ws)

    # populate unit worksheet as well
    unit_range_str = calculate_range(barcodes, unit_ws)
    unit_values = prep_values_for_unit_ws_update(barcodes)
    unit_ws.add_rows(len(barcodes))
    add_barcodes_to_worksheet(unit_range_str, unit_values, unit_ws)


def add_barcodes_to_worksheet(
    range_str: str,
    values: Union[list[tuple[str, str]], list[tuple[str]]],
    ws: gspread.worksheet.Worksheet,
) -> None:
    """Add a barcode to a given worksheet."""
    ws.batch_update([{"range": range_str, "values": values}])


def calculate_range(barcodes: list[str], worksheet: gspread.worksheet.Worksheet) -> str:
    """Calculate the range for the worksheet."""
    # Get the last row in the worksheet
    last_row = len(worksheet.get_all_values()) + 1
    # Calculate the range for the A and B columns
    range_str = f"A{last_row}:B{last_row + len(barcodes)}"
    return range_str


def create_worksheet(
    name: str, sheet: gspread.spreadsheet.Spreadsheet, rows: int
) -> gspread.worksheet.Worksheet:
    """Create a new worksheet."""
    return sheet.add_worksheet(title=name, rows=rows, cols=5)


def determine_new_barcodes(
    sh: gspread.spreadsheet.Spreadsheet, batch_size=int
) -> list[str]:
    """Generate a batch of new barcodes.

    Args:
        sh (gspread.spreadsheet.Spreadsheet): gspread Spreadsheet instance to
            pull the last barcode from.
        batch_size (int): Number of barcodes to generate.

    Returns:
        list[str]: List of generated barcodes.
    """
    last_barcode = get_last_barcode(sh)
    starting_sequence = determine_starting_sequence(last_barcode)
    return list(
        mint_barcodes(starting_sequence=starting_sequence, batch_size=batch_size)
    )


def get_creds() -> Path:
    """Get the credentials for Google Sheets API."""
    fh = Path.home() / ".cred/.gsheet/google-sheet-virtual-barcodes.json"
    return fh


def get_default_sheet_id() -> Any:
    """Get the default virtual barcodes Google Sheet ID."""
    sheet_id_fh = Path.home() / ".cred/.gsheet/default-virtual-barcodes-sheet-id.json"
    with open(sheet_id_fh) as f:
        data = json.load(f)
    return data["key"]


def get_last_barcode(sh: gspread.spreadsheet.Spreadsheet) -> str:
    """Get the last barcode from the Google Sheet.

    Args:
        sh (gspread.spreadsheet.Spreadsheet): gspread Spreadsheet instance.

    Returns:
        str: The last barcode in the sheet.
    """
    ws = get_worksheet_by_name("barcodes-to-date", sh)
    values = ws.get_all_values()
    if values:
        try:
            return values[-1][0].strip()
        except IndexError:
            return ""
    else:
        return ""


def get_sheet(key: str = "") -> gspread.spreadsheet.Spreadsheet:
    """Get the virtual barcodes Google Sheet as gspread Spreadsheet object."""
    cred_fh = get_creds()
    gc = gspread.oauth(credentials_filename=cred_fh)

    if not key:
        key = get_default_sheet_id()
    sh = gc.open_by_key(key)
    return sh


def get_worksheet_by_name(
    name: str, sheet: gspread.spreadsheet.Spreadsheet
) -> gspread.worksheet.Worksheet:
    """Get a worksheet by name."""
    return sheet.worksheet(name)


def prep_values_for_main_ws_update(
    barcodes: list[str], unit_code: str
) -> list[tuple[str, str]]:
    """Prepare data for batch update of the barcodes-to-date worksheet (main)."""
    return [(b, unit_code) for b in barcodes]


def prep_values_for_unit_ws_update(barcodes: list[str]) -> list[tuple[str]]:
    """Prepare data for batch update of the unit worksheet."""
    return [(b,) for b in barcodes]

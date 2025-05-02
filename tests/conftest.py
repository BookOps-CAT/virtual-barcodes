import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def test_sheet_id() -> Any:
    """Fixture to get the test Google Sheet ID."""
    fh = Path.home() / ".cred/.gsheet/dev-virtual-barcodes-sheet-id.json"
    with open(fh) as f:
        data = json.load(f)
    return data["key"]

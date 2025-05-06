[![Build Status](https://github.com/BookOps-CAT/virtual-barcodes/actions/workflows/unit-tests.yaml/badge.svg?branch=main)](https://github.com/BookOps-CAT/virtual-barcodes/actions) [![Coverage Status](https://coveralls.io/repos/github/BookOps-CAT/virtual-barcodes/badge.svg?branch=main)](https://coveralls.io/github/BookOps-CAT/virtual-barcodes?branch=main) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# virtual-barcodes
 
 A tool to generate virtual barcodes to be used in NYPL Sierra.

## Version
> 0.1.0

## Installation
Clone the repository and use `poetry` to create a virtual environment and install dependencies.
```bash
poetry install --without dev
```

Or, set up a virtual environment, activate it, and install via pip:
```bash
python -m venv .venv
```
```bash
python -m pip install git+https://github.com/BookOps-CAT/virtual-barcodes.git
```

## Usage
Activate package's virtual environment.

Mint new barcodes:
```bash
barcodes mint [unit code] [number of barcodes to produce]
```

Example, this command will create 200 barcodes, assign them to MSU, and output them to the NYPL virtual barcodes Google Sheet:
```bash
barcodes mint MSU 200
```


## References
+ [Sierra barcode documentation](https://ilsstaff.nypl.org:63100/sierra/admin/help/Content/sgcir/sgcir_appen_noteonbarcodes.html#barcode_patterns)
  + note when the difference in the step number 4 (10 - unit digit from the previous step) is 10, use the unit digit "0"
## Changelog 
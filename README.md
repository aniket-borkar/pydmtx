# PyDMTX: Open-Source Data Matrix ECC200 Library

PyDMTX is a from-scratch implementation of Data Matrix (DMTX) barcode encoding and decoding following the ECC200 standard (ISO/IEC 16022). It does not use any external barcode libraries and relies only on standard Python, NumPy, and Pillow.

## Installation
pip install .

## Usage
### Encoding
```python
from pydmtx import encode
matrix = encode("Hello World")
# matrix is a 2D NumPy array (1=black, 0=white)
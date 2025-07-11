# PyDMTX: Open-Source Data Matrix ECC200 Library

PyDMTX is a pure Python implementation of Data Matrix (DMTX) barcode encoding and decoding following the ECC200 standard (ISO/IEC 16022). It's built from scratch without any external barcode libraries, relying only on NumPy and Pillow for array operations and image handling.

## Features

- ✅ **Pure Python Implementation** - No external barcode libraries required
- ✅ **ECC200 Standard Compliant** - Follows ISO/IEC 16022 specification
- ✅ **Encoding Support** - Convert text/data to Data Matrix barcodes
- ✅ **Decoding Support** - Extract data from Data Matrix images
- ✅ **Reed-Solomon Error Correction** - Built-in error correction capability
- ✅ **Multiple Symbol Sizes** - Supports both square and rectangular formats
- ✅ **Image Generation** - Direct PNG output for encoded barcodes

## Installation

### From Source
```bash
git clone https://github.com/aniket-borkar/pydmtx.git
cd pydmtx
pip install .
```

### Dependencies
- Python 3.6+
- NumPy
- Pillow

## Quick Start

### Encoding
```python
from pydmtx import encode

# Basic encoding - returns a 2D NumPy array
matrix = encode("Hello World")
# matrix is a 2D NumPy array where 1=black, 0=white

# Generate barcode image directly
matrix = encode("Hello World", generate_image=True)
# Saves as 'barcode.png' in current directory
```

### Decoding
```python
from pydmtx import decode

# Decode from image file
data = decode("barcode.png")
print("Decoded:", data)  # Output: "Hello World"

# Decode from NumPy array
import numpy as np
matrix = np.array([[1, 0, 1, ...], ...])  # Your barcode matrix
data = decode(matrix)
```

## API Reference

### `encode(data, generate_image=False)`
Encodes data into a Data Matrix barcode.

**Parameters:**
- `data` (str): The data to encode
- `generate_image` (bool): If True, saves the barcode as 'barcode.png'

**Returns:**
- `numpy.ndarray`: 2D array representing the barcode (1=black, 0=white)

**Raises:**
- `ValueError`: If data is too long for any supported symbol size

### `decode(input_data)`
Decodes a Data Matrix barcode.

**Parameters:**
- `input_data`: Either a file path (str) to an image or a NumPy array

**Returns:**
- `str`: The decoded data

**Raises:**
- `ValueError`: If the symbol size is not supported

## Supported Symbol Sizes

PyDMTX supports the following ECC200 symbol sizes:

### Square Symbols
- 10×10 through 144×144 (24 sizes)
- Data capacity: 3 to 1558 data codewords
- Error correction: 5 to 620 EC codewords

### Rectangular Symbols
- 8×18, 8×32, 12×26, 12×36, 16×36, 16×48
- Data capacity: 10 to 98 data codewords
- Error correction: 10 to 56 EC codewords

## Technical Details

### Encoding Process
1. **Data Analysis**: Converts input data to codewords (currently using ASCII mode)
2. **Size Selection**: Automatically selects the smallest symbol size that fits the data
3. **Padding**: Adds padding codewords (129) if needed
4. **Error Correction**: Applies Reed-Solomon error correction
5. **Module Placement**: Places data and EC codewords in the symbol matrix
6. **Finder Pattern**: Adds the distinctive L-shaped finder pattern

### Decoding Process
1. **Image Processing**: Converts image to binary matrix (black=1, white=0)
2. **Pattern Detection**: Identifies symbol size from dimensions
3. **Bit Extraction**: Extracts data bits from the matrix
4. **Error Correction**: Applies Reed-Solomon error correction
5. **Data Interpretation**: Converts codewords back to original data

### Current Limitations
- Encoding uses simplified ASCII mode (full C40/TEXT/BASE256 modes planned)
- Decoding assumes upright orientation (rotation detection planned)
- Fixed output filename for image generation

## Examples

Check the `examples/` directory for complete working examples:
- `encode_example.py` - Basic encoding with image generation
- `decode_example.py` - Decoding from image file

## Contributing

Contributions are welcome! This is an open-source project under active development. Areas for improvement include:
- Full encoding mode support (C40, TEXT, BASE256)
- Automatic rotation detection in decoder
- Structured append support
- Performance optimizations

## License

MIT License - see LICENSE file for details

## Author

Aniket Borkar - aniket.borkar@gmail.com

## Links

- GitHub: https://github.com/aniket-borkar/pydmtx
- ISO/IEC 16022 Standard: [Data Matrix specification](https://www.iso.org/standard/44230.html)

import numpy as np
from .rs import rs_correct_msg
from .encoder import SYMBOL_SIZES  # <-- FIX: Import SYMBOL_SIZES from encoder

def decode(input_data):
    if isinstance(input_data, str):
        from PIL import Image
        img = Image.open(input_data).convert('L')
        # In Data Matrix: black pixels (low values) = 1, white pixels (high values) = 0
        matrix = np.array(img) < 128  # Changed from > to <
    else:
        matrix = input_data

    # Step 1: Detect finder pattern and orientation (simplified, assume upright)
    rows, cols = matrix.shape

    # Find data_cw, ec_cw from size (FIX: Now uses imported SYMBOL_SIZES)
    data_cw, ec_cw = None, None
    for r, c, d, e in SYMBOL_SIZES:
        if r == rows and c == cols:
            data_cw, ec_cw = d, e
            break
    if data_cw is None:
        raise ValueError("Unsupported symbol size")

    # Step 2: Extract bits (simplified)
    bits = []
    total_bits = (data_cw + ec_cw) * 8
    for y in range(rows - 2, 0, -2):
        for x in range(cols - 1, -1, -1):
            for yy in [y, y-1]:
                if len(bits) < total_bits and 1 <= x <= cols - 2 and 1 <= yy <= rows - 2:
                    bits.append(matrix[yy, x])

    # Convert to codewords
    codewords = []
    for i in range(0, len(bits), 8):
        cw = 0
        for j in range(8):
            if i + j < len(bits):
                cw = (cw << 1) | bits[i + j]
        codewords.append(cw)

    # Step 3: RS correction
    data = rs_correct_msg(codewords, ec_cw)

    # Step 4: Decode modes (simplified ASCII)
    result = ''
    for cw in data:
        # Handle special codewords
        if cw == 232:  # FNC1
            continue
        if cw == 129:  # Pad character - stop decoding
            break
        if cw == 0:  # Invalid codeword
            continue
            
        # Decode ASCII (codeword value = ASCII value + 1)
        if 1 <= cw <= 128:
            result += chr(cw - 1)
        # For now, ignore other modes (C40, TEXT, etc.)
        # In a full implementation, we would handle mode switches
        
    return result
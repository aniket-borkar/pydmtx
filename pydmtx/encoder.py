import numpy as np
from .rs import rs_encode_msg

# Full ECC200 symbol sizes (rows, cols, data codewords, ec codewords)
# Compiled from ISO/IEC 16022: square and rectangular
SYMBOL_SIZES = [
    # Square
    (10, 10, 3, 5),
    (12, 12, 5, 7),
    (14, 14, 8, 10),
    (16, 16, 12, 12),
    (18, 18, 18, 14),
    (20, 20, 22, 18),
    (22, 22, 30, 20),
    (24, 24, 36, 24),
    (26, 26, 44, 28),
    (32, 32, 62, 36),
    (36, 36, 86, 42),
    (40, 40, 114, 48),
    (44, 44, 144, 56),
    (48, 48, 174, 68),
    (52, 52, 204, 84),
    (64, 64, 280, 112),
    (72, 72, 368, 144),
    (80, 80, 456, 192),
    (88, 88, 576, 224),
    (96, 96, 696, 272),
    (104, 104, 816, 336),
    (120, 120, 1050, 408),
    (132, 132, 1304, 496),
    (144, 144, 1558, 620),
    # Rectangular
    (8, 18, 10, 10),
    (8, 32, 20, 16),
    (12, 26, 32, 24),
    (12, 36, 44, 28),
    (16, 36, 64, 44),
    (16, 48, 98, 56),
]

# Encoding modes (unchanged)
MODE_ASCII = 0
MODE_C40 = 1
MODE_TEXT = 2
MODE_BASE256 = 3

# C40 encoding table (partial, expand as needed)
C40_VALUES = {
    '0': 3, '1': 4, '2': 5, '3': 6, '4': 7, '5': 8, '6': 9, '7': 10, '8': 11, '9': 12,
    'A': 14, 'B': 15, # ... full table in spec
    # Add all
}

def encode(data, generate_image=False):
    # Step 1: Determine optimal mode (simplified to ASCII for now)
    codewords = []
    for char in data:
        codewords.append(ord(char) + 1)  # ASCII

    # Add FNC1 if GS1
    if data.startswith('('):  # Simplified GS1 check
        codewords.insert(0, 232)

    # Step 2: Determine symbol size
    num_cw = len(codewords)
    selected = None
    for rows, cols, data_cw, ec_cw in SYMBOL_SIZES:
        if num_cw <= data_cw:
            selected = (rows, cols, data_cw, ec_cw)
            break
    if not selected:
        raise ValueError("Data too long")
    rows, cols, data_cw, ec_cw = selected

    # Pad with 129 if needed
    while len(codewords) < data_cw:
        codewords.append(129)

    # Step 3: Reed-Solomon
    encoded = rs_encode_msg(codewords, ec_cw)

    # Step 4: Module placement (simplified for square; extend for rect)
    modules = np.zeros((rows, cols), dtype=int)
    # Finder pattern (adjust for rect if needed)
    modules[-1, :] = 1  # Bottom solid
    modules[:, 0] = 1  # Left solid
    for i in range(cols):
        modules[0, i] = i % 2  # Top alternating
    for i in range(rows):
        modules[i, -1] = (i + 1) % 2  # Right alternating

    # Place data bits
    bit_idx = 0
    total_bits = len(encoded) * 8
    for y in range(rows - 2, 0, -2):
        for x in range(cols - 1, -1, -1):
            for yy in [y, y-1]:
                if 1 <= x <= cols - 2 and 1 <= yy <= rows - 2 and modules[yy, x] == 0 and bit_idx < total_bits:
                    bit = (encoded[bit_idx // 8] >> (7 - bit_idx % 8)) & 1
                    modules[yy, x] = bit
                    bit_idx += 1

    if generate_image:
        from PIL import Image
        # Invert the colors: 1 (black) -> 0, 0 (white) -> 255
        img_data = (1 - modules) * 255
        img = Image.fromarray(img_data.astype(np.uint8), 'L')
        img.save('barcode.png')

    return modules
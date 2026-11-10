#!/usr/bin/env python3

"""
Read a 256x128 pixel BMP file where each 8x16 block represents a character glyph.
Convert it to a 4096-byte binary file where each byte represents one line of a character (8 pixels).
The output can be in .bin, .hex or .mif format for use in FPGA
"""

import struct
import argparse

from convert import generate_mem, generate_mif

# a single character is 8x16 pixels, so the whole font is 256x128 pixels:
FONT_WIDTH = 8
FONT_HEIGHT = 16

IMAGE_WIDTH = 256
IMAGE_HEIGHT = 128

def transform_to_font_bytes(bits) -> bytes:
    """
    Convert bits[128][256] to byte[4096].
    4096 = 256 characters * 16 lines per character.
    Each element is a list of 8 bits.
    """
    CHARS_PER_ROW = 32
    CHAR_WIDTH = 8
    CHAR_HEIGHT = 16
    ROWS_OF_CHARS = 8

    font_bytes = []

    for row_idx in range(ROWS_OF_CHARS):
        y_offset = row_idx * CHAR_HEIGHT
        for char_idx in range(CHARS_PER_ROW):
            x_offset = char_idx * CHAR_WIDTH
            for y in range(CHAR_HEIGHT):
                # get 8 bits for this line of the character:
                line_pixels = bits[y_offset + y][x_offset : x_offset + CHAR_WIDTH]
                # convert 8 bits to a byte value (MSB at index 0)
                # [1, 0, 0, 1, 0, 0, 0, 0] -> 0x90
                byte_val = 0
                for bit in line_pixels:
                    byte_val = (byte_val << 1) | bit
                font_bytes.append(byte_val)
    return bytes(font_bytes)

def read_bmp_to_bits(file_path):
    with open(file_path, 'rb') as f:
        # --- parse file header ---
        magic = f.read(2)
        if magic != b'BM':
            print(f"Error: invalid BMP magic number {magic}.")
            exit(1)

        # skip 8 bytes
        f.seek(8, 1) 

        # pixel offset: 4 bytes, little endian:
        pixel_offset = struct.unpack('<I', f.read(4))[0]

        # --- parse DIB header ---
        # skip header size: 4 bytes:
        f.seek(4, 1)
        # read width, height, depth:
        width, height, _, bit_depth = struct.unpack('<iiHH', f.read(12))
        if width != IMAGE_WIDTH or height != IMAGE_HEIGHT:
            print(f"Error: expected dimensions {IMAGE_WIDTH}x{IMAGE_HEIGHT}, but got {width}x{height}.")
            exit(1)

        if bit_depth != 24:
            print(f"Error: expected 24-bit BMP, but got {bit_depth}-bit.")
            exit(1)

        # --- read pixel data ---
        f.seek(pixel_offset)

        # scan BMP pixel data from bottom to top, and convert to bits[128][256]:
        bytes_per_pixel = bit_depth // 8
        row_size = (width * bytes_per_pixel + 3) & ~3 # 向上取 4 的倍数
        
        # BMP stores pixels from bottom to top
        raw_rows = []
        for _ in range(height):
            row_data = f.read(row_size)
            pixels_in_row = []
            for x in range(width):
                start = x * bytes_per_pixel
                b, g, r = row_data[start:start+3]
                # Binarize: 1 for white, 0 for black
                is_white = 1 if (r + g + b) // 3 > 128 else 0
                pixels_in_row.append(is_white)
            raw_rows.append(pixels_in_row)

        # --- Convert to bits[row][col] (i.e., bits[128][256]) ---
        # BMP data in raw_rows is index 0 = bottom row. 
        # We want bits[0] = top row.
        bits = []
        for y in range(height):
            # Reverse the row index to get top-down order
            bits.append(raw_rows[height - 1 - y])
        return bits

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate font binary data from bitmap.')
    parser.add_argument('-i', '--input', required=False, type=str, metavar='font.bmp', default="font.bmp",
                        help='bmp as input file.')
    args = parser.parse_args()
    try:
        print(f'Reading BMP file: {args.input}')
        if not args.input.endswith('.bmp'):
            print("Error: input file must be a BMP image.")
            exit(1)

        bits = read_bmp_to_bits(args.input)
        data = transform_to_font_bytes(bits)

        output_file = args.input[:-4]
        generate_mif(data, 1, f'{output_file}.mi')
        print(f"Generated {output_file}.mi ok.")
        generate_mif(data, 1, f'{output_file}.mif')
        print(f"Generated {output_file}.mif ok.")
        generate_mem(data, 1, f'{output_file}.hex')
        print(f"Generated {output_file}.hex ok.")
        generate_mem(data, 1, f'{output_file}.bin')
        print(f"Generated {output_file}.bin ok.")
    except IOError as e:
        print(f"Error: {e}")

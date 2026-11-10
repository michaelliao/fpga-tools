# Tools for generating hex data

## How to generate font data for ROM

Use Photoshop to edit source file and export to 256x128 24-bit bitmap:

`font.psd` -> `font.bmp`

Each character takes 8x16 bitmap pixels.

Use command `python convert_font_rom.py` to convert `font.bmp` to files that EDA tools can load:

```plain
font.bmp -> font.hex (simulation)
         -> font.bin
         -> font.mif (Quartus)
         -> font.mi (Gowin)
```

## How to generate screen data for RAM

The characters in screen is `80 x 25 = 2000`. Each character takes 1 byte ASCII + 1 byte color attribute = 2 bytes, 
so the total bytes is `80 x 25 x 2 = 4000` bytes.

The plain source file is `screen_plain.txt`.

The source file with background / foreground color is `screen.txt`.

You can change the content of the text file.

Use command `python convert_screen.py` to convert `screen.txt` to files that EDA tools can load:

```plain
screen.txt -> screen.hex (simulation)
           -> screen.mif (Quartus)
           -> screen.mi  (Gowin)
```

The output data width is 16 and address range is `0x000` ~ `0x7CF`.

The `screen_4k.*` files are also generated to simulate a 4KB page data in DDR. It just appends `0x00` at index of `[4000 ~ 4096)`.

The 4k output data width is 32 and address range is `0x000` ~ `0x3FF`.

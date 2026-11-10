#!/usr/bin/env python3

def generate_mem(data: bytes, nBytes: int, output_file: str):
    """
    Convert bytes to a text file where each line is nBytes (binary or hex).
    """
    data_len = len(data)
    if data_len % nBytes != 0:
        print(f"Error: Data length ({data_len}) is not a multiple of nBytes ({nBytes}).")
        exit(1)
    width = 8 * nBytes
    depth = data_len // nBytes
    is_hex = output_file.endswith('.hex')
    with open(output_file, 'w', newline='\n') as f:
        f.write(f"// {data_len} bytes, address 0x0 ~ 0x{depth - 1:x}, width = {width}\n")
        for i in range(0, data_len, nBytes):
            chunk = data[i : i + nBytes]
            if is_hex:
                # b'\x07\x41' (nBytes=2) -> "0741"
                hex_str = "".join(f"{b:02x}" for b in chunk)
                f.write(f"{hex_str}\n")
            else:
                # b'\x07\x41' (nBytes=2) -> "0000011101000001"
                bin_str = "".join(f"{b:08b}" for b in chunk)
                f.write(f"{bin_str}\n")

def generate_mif(data: bytes, nBytes: int, output_file: str, output_hex: bool = False):
    """
    Convert bytes to MIF/MI format.
    """
    data_len = len(data)
    if data_len % nBytes != 0:
        print(f"Error: Data length ({data_len}) is not a multiple of nBytes ({nBytes}).")
        exit(1)
    width = 8 * nBytes
    depth = data_len // nBytes
    is_mif = output_file.endswith('.mif')

    with open(output_file, 'w', newline='\n') as f:
        if is_mif:
            # MIF header:
            f.write(f"-- {data_len} bytes, address 0x0 ~ 0x{depth - 1:x}, width = {width}\n")
            f.write(f"WIDTH = {width};\n")
            f.write(f"DEPTH = {depth};\n")
            f.write("ADDRESS_RADIX = HEX;\n")
            f.write(f"DATA_RADIX = {'HEX' if output_hex else 'BIN'};\n")
            f.write("CONTENT BEGIN\n")
        else:
            # MI header:
            f.write(f"#File_format={'Hex' if output_hex else 'Bin'}\n")
            f.write(f"#Address_depth={depth}\n")
            f.write(f"#Data_width={width}\n")
        for addr in range(depth):
            start = addr * nBytes
            end = start + nBytes
            chunk = data[start:end]
            if output_hex:
                # chunk = [0x70, 0x41] -> "7041"
                out_str = "".join(f"{b:02x}" for b in chunk)
            else:
                # chunk = [0x70, 0x41] -> "0111000001000001"
                out_str = "".join(f"{b:08b}" for b in chunk)
            if is_mif:
                # write address : data;
                f.write(f"{addr:03x} : {out_str};\n")
            else:
                # write data:
                f.write(f"{out_str}\n")

        if is_mif:
            f.write("END;\n")

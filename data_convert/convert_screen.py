#!/usr/bin/env python3

import argparse
import re

from convert import generate_mem, generate_mif

def load_text_as_bytes(input_txt: str) -> bytes:
    """
    解析带 ANSI 转义序列的文本并转换为 4000 字节的 VRAM 数据。
    每字符 2 字节：[Attribute, ASCII]
    """
    # 读取整个文件内容
    with open(input_txt, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    print(content)

    # ANSI 转义序列匹配正则: \033[...m
    ansi_re = re.compile(r'\x1b\[([0-9;]*)m')
    
    vram_data = bytearray()
    
    # 默认属性: 0x07 (黑底白字)
    current_fg = 7  # Light Gray
    current_bg = 0  # Black
    
    # 将内容按行分割，最多取 25 行
    lines = content.splitlines()[:25]
    
    for row in range(25):
        line = lines[row] if row < len(lines) else ""
        
        # 这一行解析后的字符对列表
        row_pairs = []
        
        # 使用正则表达式寻找所有转义序列的位置
        last_end = 0
        for match in ansi_re.finditer(line):
            # 1. 处理转义序列之前的普通文本
            text_part = line[last_end:match.start()]
            for char in text_part:
                attr = (current_bg << 4) | (current_fg & 0x0F)
                row_pairs.append((attr, ord(char)))
            
            # 2. 处理转义序列，更新颜色状态
            params = match.group(1).split(';')
            for p in params:
                p_val = int(p) if p else 0
                if p_val == 0:        # Reset
                    current_fg, current_bg = 7, 0
                elif 30 <= p_val <= 37: # Foreground
                    current_fg = p_val - 30
                elif 40 <= p_val <= 47: # Background
                    current_bg = p_val - 40
                elif p_val == 1:      # Bold (VGA 中通常表现为高亮度)
                    current_fg |= 0x08
            
            last_end = match.end()
            
        # 处理剩余的文本
        for char in line[last_end:]:
            attr = (current_bg << 4) | (current_fg & 0x0F)
            row_pairs.append((attr, ord(char)))

        # 3. 填充或截断至 80 列
        for col in range(80):
            if col < len(row_pairs):
                attr, ascii_val = row_pairs[col]
            else:
                # 默认补空格，保持当前行末尾颜色属性或默认属性
                attr = (current_bg << 4) | (current_fg & 0x0F)
                ascii_val = 0x20 
            
            vram_data.append(attr)
            vram_data.append(ascii_val)

    # 如果不满 25 行，填充后续显存空间
    while len(vram_data) < 4000:
        vram_data.append(0x07)
        vram_data.append(0x20)

    return bytes(vram_data[:4000])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate font binary data from bitmap.')
    parser.add_argument('-i', '--input', required=False, type=str, metavar='screen.txt', default="screen.txt",
                        help='text file as input.')
    args = parser.parse_args()

    try:
        print(f'Reading text file: {args.input}')
        data = load_text_as_bytes(args.input)
        
        output_file = args.input[:-4]
        generate_mif(data, 2, f'{output_file}.mi', output_hex=True)
        print(f"Generated {output_file}.mi ok.")
        generate_mif(data, 2, f'{output_file}.mif', output_hex=True)
        print(f"Generated {output_file}.mif ok.")
        generate_mem(data, 2, f'{output_file}.hex')
        print(f"Generated {output_file}.hex ok.")
        generate_mem(data, 2, f'{output_file}.bin')
        print(f"Generated {output_file}.bin ok.")

        # fill with 4K:
        while len(data) < 4096:
            data += b'\x00'
        output_4k = output_file + "_4k"
        generate_mif(data, 4, f'{output_4k}.mi', output_hex=True)
        print(f"Generated {output_4k}.mi ok.")
        generate_mif(data, 4, f'{output_4k}.mif', output_hex=True)
        print(f"Generated {output_4k}.mif ok.")
        generate_mem(data, 4, f'{output_4k}.hex')
        print(f"Generated {output_4k}.hex ok.")
        generate_mem(data, 4, f'{output_4k}.bin')
        print(f"Generated {output_4k}.bin ok.")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import argparse, configparser

def load_config(ini_file):
    print(f'load config {ini_file}...')
    config = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
    config.read(ini_file, encoding='utf-8')
    definitions = {}
    for port in config.sections():
        names = config.get(port, 'names', fallback='')
        description = config.get(port, 'description', fallback='')
        if not names:
            print(f'WARN: missing "names" for port {port}.')
            continue
        if not description:
            print(f'WARN: missing "description" for port {port}.')
            continue
        name_list = [name.strip() for name in names.lower().split(',') if name.strip()]
        for name in name_list:
            if name in definitions:
                print(f'WARN: duplicate name "{name}" found.')
            else:
                definitions[name] = (port, description)
    return definitions

import re

def extract_and_expand_ports(verilog_code):
    # remove comments:
    clean_code = re.sub(r'/\*.*?\*/', '', verilog_code, flags=re.DOTALL)
    clean_code = re.sub(r'//.*', '', clean_code)
    # match the ports section of the module declaration:
    ports_section_match = re.search(r'module\s+\w+(?:\s*#\(.*?\))?\s*\((.*?)\);', clean_code, re.DOTALL)
    if not ports_section_match:
        print("Warning: No valid module port declaration structure found.")
        return []
        
    ports_text = ports_section_match.group(1)
    port_pattern = re.compile(
        r'(?:input|output|inout)\s+'
        r'(?:(?:\w+)\s+)*' # type: logic, wire
        r'(?:\[\s*(\d+)\s*:\s*(\d+)\s*\]\s*)?'
        r'(\w+)'
    )

    expanded_ports = []
    # process ports:
    for match in port_pattern.finditer(ports_text):
        msb_str, lsb_str, port_name = match.groups()
        if msb_str is not None and lsb_str is not None:
            msb = int(msb_str)
            lsb = int(lsb_str)
            step = -1 if msb >= lsb else 1
            min_val = min(msb, lsb)
            max_val = max(msb, lsb)
            for i in range(min_val, max_val + 1):
                expanded_ports.append(f"{port_name}[{i}]")
        else:
            expanded_ports.append(port_name)
    return expanded_ports

def get_diff_pair_name(port_name, port_names):
    base_names = []
    if port_name.lower().endswith("_n"):
        base_names = [port_name[:-2] + "_p", port_name[:-2]]
    else:
        pos = port_name.lower().find("_n[")
        if pos > 0:
            base_names = [port_name[:pos] + "_p" + port_name[pos + 2:], port_name[:pos] + port_name[pos + 2:]]
    port_names_lower = [p.lower() for p in port_names]
    for base_name in base_names:
        if base_name.lower() in port_names_lower:
            return base_name
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read port definition from Markdown file and update CST file accordingly.")
    parser.add_argument("-ini", metavar="<ini_file>", required=True, help="Config file (.ini) containing the port definitions.")
    parser.add_argument("-v", metavar="<verilog_file>", required=True, help="Verilog file (.v or .sv) containing the module declaration.")
    parser.add_argument("-cst", metavar="<cst_file>", required=True, help="CST file (.cst) to be updated with the port definitions.")

    args = parser.parse_args()
    port_definitions = load_config(args.ini)

    with open(args.v, 'r', encoding='utf-8') as f:
        verilog_code = f.read()
    port_names = extract_and_expand_ports(verilog_code)
    cst_lines = ["// Auto-generated CST file:", ""]
    print(f"Ports: {', '.join(port_names)}")
    for port_name in port_names:
        if port_name.lower() in port_definitions:
            port, port_type = port_definitions[port_name.lower()]
            cst_lines.append(f'IO_LOC "{port_name}" {port};')
            cst_lines.append(f'IO_PORT "{port_name}" {port_type};')
            cst_lines.append("")
        else:
            diff_port = get_diff_pair_name(port_name, port_names)
            if diff_port and (diff_port.lower() in port_definitions) and (port_definitions[diff_port.lower()][0].find(",") >= 0):
                cst_lines.append(f'// diff_port: {port_name} <--> {diff_port}')
                cst_lines.append("")
            else:
                cst_lines.append(f"// WARN: port {port_name} not found in the config file.")
                cst_lines.append("")
                continue
    content = "\n".join(cst_lines)
    with open(args.cst, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"CST file '{args.cst}' has been generated:")
    print(content)

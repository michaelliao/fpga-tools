# GOWIN FPGA Floor Planner Tool

<a id="en"></a>

[中文](#chs) | English

Generate GoWin FPGA floor planner file:

```plain
$ python3 floor_planner.py \
  -ini board/Xiaomeige_ACG720_60K_GW5AT-LV60PG484A.ini \
  -v test/top.sv \
  -cst test/hdmi.cst
```

Parameters:

- `-ini`: specify `ini` file that describes the ports on board;
- `-v`: specify top module file (Verilog or SystemVerilog);
- `-cst`: specify the generated `cst` file.

## IO Ports Description File

The IO ports are defined in `ini` file. For example:

```ini
[Y18]
names = sys_clk, clk
description = IO_TYPE=LVCMOS33 PULL_MODE=UP BANK_VCCIO=3.3

[B21]
names = sys_rst_n, rst_n
description = IO_TYPE=LVCMOS33 PULL_MODE=UP BANK_VCCIO=3.3

[K4,J4]
names = o_tmds_clk_p, tmds_clk_p
description = IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3

[L3,K3]
names = o_tmds_data_p[0], tmds_data_p[0]
description = IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3

[L5,L4]
names = o_tmds_data_p[1], tmds_data_p[1]
description = IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3

[M3,M2]
names = o_tmds_data_p[2], tmds_data_p[2]
description = IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3
```

The script extracts the ports from top module and generate the `cst` file by name matching:

```plain
IO_LOC "sys_clk" Y18;
IO_PORT "sys_clk" IO_TYPE=LVCMOS33 PULL_MODE=NONE BANK_VCCIO=3.3;

IO_LOC "sys_rst_n" B21;
IO_PORT "sys_rst_n" IO_TYPE=LVCMOS33 PULL_MODE=NONE BANK_VCCIO=3.3;

IO_LOC "tmds_clk_p" K4,J4;
IO_PORT "tmds_clk_p" IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3;

// diff_port: tmds_clk_n <--> tmds_clk_p

IO_LOC "tmds_data_p[0]" L3,K3;
IO_PORT "tmds_data_p[0]" IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3;

IO_LOC "tmds_data_p[1]" L5,L4;
IO_PORT "tmds_data_p[1]" IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3;

IO_LOC "tmds_data_p[2]" M3,M2;
IO_PORT "tmds_data_p[2]" IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3;

// diff_port: tmds_data_n[0] <--> tmds_data_p[0]

// diff_port: tmds_data_n[1] <--> tmds_data_p[1]

// diff_port: tmds_data_n[2] <--> tmds_data_p[2]
```

Diff port is auto-detected by script.

---

<a id="chs"></a>

[English](#en) | 中文

生成高云FPGA布线文件：

```plain
$ python3 floor_planner.py \
  -ini board/Xiaomeige_ACG720_60K_GW5AT-LV60PG484A.ini \
  -v test/top.sv \
  -cst test/hdmi.cst
```

参数说明:

- `-ini`：指定描述端口的`ini`文件；
- `-v`：指定Verilog或SystemVerilog的顶层模块文件；
- `-cst`：指定要输出的`cst`文件。

## IO端口描述文件

IO端口描述定义在`ini`文件中。示例：

```ini
[Y18]
names = sys_clk, clk
description = IO_TYPE=LVCMOS33 PULL_MODE=UP BANK_VCCIO=3.3

[B21]
names = sys_rst_n, rst_n
description = IO_TYPE=LVCMOS33 PULL_MODE=UP BANK_VCCIO=3.3

[K4,J4]
names = o_tmds_clk_p, tmds_clk_p
description = IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3

[L3,K3]
names = o_tmds_data_p[0], tmds_data_p[0]
description = IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3

[L5,L4]
names = o_tmds_data_p[1], tmds_data_p[1]
description = IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3

[M3,M2]
names = o_tmds_data_p[2], tmds_data_p[2]
description = IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3
```

脚本会自动从模块中提取端口定义，然后根据名称生成`cst`文件：

```plain
IO_LOC "sys_clk" Y18;
IO_PORT "sys_clk" IO_TYPE=LVCMOS33 PULL_MODE=NONE BANK_VCCIO=3.3;

IO_LOC "sys_rst_n" B21;
IO_PORT "sys_rst_n" IO_TYPE=LVCMOS33 PULL_MODE=NONE BANK_VCCIO=3.3;

IO_LOC "tmds_clk_p" K4,J4;
IO_PORT "tmds_clk_p" IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3;

// diff_port: tmds_clk_n <--> tmds_clk_p

IO_LOC "tmds_data_p[0]" L3,K3;
IO_PORT "tmds_data_p[0]" IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3;

IO_LOC "tmds_data_p[1]" L5,L4;
IO_PORT "tmds_data_p[1]" IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3;

IO_LOC "tmds_data_p[2]" M3,M2;
IO_PORT "tmds_data_p[2]" IO_TYPE=LVCMOS33D PULL_MODE=NONE DRIVE=8 BANK_VCCIO=3.3;

// diff_port: tmds_data_n[0] <--> tmds_data_p[0]

// diff_port: tmds_data_n[1] <--> tmds_data_p[1]

// diff_port: tmds_data_n[2] <--> tmds_data_p[2]
```

差分端口由脚本自动检测。

# 函数列表目录

此目录用于存放各个项目的函数列表文件。

## 文件命名规范

- 文件名：`<项目名>.txt`
- 每行一个函数文件路径（相对于项目根目录）
- 支持注释（以`#`开头的行）

## 示例

### can.txt
```
FUN/CAN_Read_Data_SWMC.st
FUN/CAN_Send_Data_SWMC.st
```

### 使用方法

```bash
python project_gen.py -p "st项目代码提取/重型运输系统/can" -l function_lists/can.txt -n can
```

## 目录结构

```
function_lists/
├── README.md          # 本文件
├── can.txt           # CAN模块函数列表
├── core.txt          # Core模块函数列表（示例）
├── modbus.txt        # Modbus模块函数列表（示例）
└── ...               # 其他项目的函数列表
```

## 文件格式示例

```
# CAN模块的函数
FUN/CAN_Read_Data_SWMC.st
FUN/CAN_Send_Data_SWMC.st

# PRG程序
PRG/CanRx_C01_Rx_method.st
PRG/CanRx_C02_Rx_method.st

# 注释行会被忽略
# PRG/CanRx_C03_Rx_method.st
```

## 路径说明

- 路径相对于 `-p` 参数指定的项目根目录
- 使用正斜杠 `/` 作为路径分隔符（跨平台兼容）
- 不要以 `/` 开头

### 正确示例 ✅
```
FUN/CAN_Read_Data_SWMC.st
PRG/CanRx.st
struct/Can_baseframe.st
```

### 错误示例 ❌
```
/FUN/CAN_Read_Data_SWMC.st          # 不要以/开头
FUN\CAN_Read_Data_SWMC.st           # 使用/而不是\
can/FUN/CAN_Read_Data_SWMC.st       # 不要包含项目名
```



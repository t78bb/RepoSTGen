# 原地修复模式说明

## 📋 改动概述

将 `full_process.py` 的修复流程改为**原地修复模式**，不再创建 `_fixed` 目录，所有操作在同一个时间戳目录中完成。

## 🎯 改动原因

**之前的问题**：
- 每次执行产生两个目录：`output/[timestamp]/` 和 `output/[timestamp]_fixed/`
- 目录冗余，占用额外空间
- 评估和后续处理需要关注 `_fixed` 目录

**改进方案**：
- 修复直接在原目录进行，只产生一个目录：`output/[timestamp]/`
- 自动备份修复前的版本到 `readful_result_before_fix`
- 历史修复记录保存在 `readful_result_history`

## 📁 目录结构对比

### ❌ 之前（两个目录）

```
output/
├── 20260121_195204/              # 生成阶段
│   └── repoeval_readwriteFile/
│       ├── readful_result/       # 生成的原始代码
│       ├── readful_result_no_provide/
│       ├── generations_*.json
│       └── results.jsonl
│
└── 20260121_195204_fixed/        # 修复阶段（新目录）
    └── repoeval_readwriteFile/
        ├── readful_result/       # 修复后的代码
        ├── readful_result_history/
        ├── generations_*.json
        └── results.jsonl
```

### ✅ 现在（一个目录）

```
output/
└── 20260121_195204/              # 生成 + 修复合并
    └── repoeval_readwriteFile/
        ├── readful_result/              # 修复后的最终代码
        ├── readful_result_before_fix/   # 自动备份：修复前的原始代码
        ├── readful_result_no_provide/   # 不含 provide_code 的版本
        ├── readful_result_history/      # 修复过程的历史记录
        ├── generations_*.json
        └── results.jsonl
```

## 🔧 技术实现

### 1. 修改 `run_fix()` 函数

```python
def run_fix(dataset_dir: Path, in_place: bool = True) -> bool:
    """
    参数:
        dataset_dir: 数据集目录
        in_place: 是否原地修复（默认 True）
    """
    if in_place:
        # 备份原始 readful_result
        backup_dir = dataset_dir / 'readful_result_before_fix'
        shutil.copytree(readful_result_dir, backup_dir)
        
        # 直接在原目录修复
        output_st_file = st_file  # 直接使用原文件
    else:
        # 旧模式：复制到新目录（保留兼容性）
        ...
```

### 2. 修改调用方式

```python
# 之前
output_fixed_dir = output_dir / f"{result_dir_name}_fixed"
fix_success = run_fix(dataset_dir, output_fixed_dir)

# 现在
fix_success = run_fix(dataset_dir, in_place=True)
```

## 📊 目录内容说明

### `readful_result/`
- **内容**：修复后的最终 ST 代码（包含 provide_code）
- **用途**：用于后续评估、部署
- **示例**：`ReadFile.st`、`WriteFile.st`

### `readful_result_before_fix/` ⭐ 新增
- **内容**：修复前的原始生成代码（自动备份）
- **用途**：对比修复前后的差异，回滚修复
- **生成时机**：每次执行修复时自动创建

### `readful_result_no_provide/` ⭐ 修改
- **内容**：修复后的代码，去除 provide_code（仅实现逻辑）
- **用途**：单独评估修复后的实现部分质量
- **生成时机**：修复阶段完成后自动创建（从修复后的 readful_result 生成）

### `readful_result_history/`
- **内容**：修复过程中每次迭代的代码版本
- **用途**：调试修复过程，分析修复路径
- **格式**：`ReadFile_v1.st`、`ReadFile_v2.st` 等

## ✅ 优势

1. **节省空间**：不再产生重复的 `_fixed` 目录
2. **简化路径**：所有结果在一个目录，便于管理
3. **自动备份**：修复前的代码自动保存，不会丢失
4. **清晰的版本历史**：
   - `readful_result_before_fix`：修复前的版本
   - `readful_result`：修复后的版本
   - `readful_result_history`：修复过程的中间版本

## 🔄 工作流程

```mermaid
graph LR
    A[生成代码] --> B[创建 readful_result]
    B --> C[备份到 readful_result_before_fix]
    C --> D[自动修复 readful_result]
    D --> E[历史版本存入 readful_result_history]
    E --> F[生成 readful_result_no_provide]
```

1. **生成阶段**：
   - 创建 `output/[timestamp]/[project]/readful_result/`（包含 provide_code）

2. **修复阶段**（原地进行）：
   - 备份：`readful_result` → `readful_result_before_fix`
   - 修复：直接修改 `readful_result` 中的文件
   - 历史：每次迭代保存到 `readful_result_history`
   - 去除定义：从修复后的 `readful_result` 生成 `readful_result_no_provide`

## 📝 使用方式

### 运行流程（无变化）

```bash
python full_process.py --project readwriteFile
```

### 输出示例

```
================================================================================
开始验证和修复: repoeval_readwriteFile
================================================================================
  ✓ 已备份原始 readful_result 到 readful_result_before_fix
  找到 2 个ST文件

  处理文件: ReadFile.st
    开始自动修复...
    ✓ 修复成功！共尝试 2 次

  处理文件: WriteFile.st
    开始自动修复...
    ✓ 修复成功！共尝试 1 次

  ✓ 修复完成: 2/2 个文件修复成功

  生成不含 provide_code 的版本...
  ✓ 已生成 readful_result_no_provide 目录，包含 2 个 ST 文件（修复后，去除 provide_code）
```

## 🔍 文件对比示例

### 查看修复前后的差异

```bash
# Windows
diff output/20260121_195204/repoeval_readwriteFile/readful_result_before_fix/ReadFile.st ^
     output/20260121_195204/repoeval_readwriteFile/readful_result/ReadFile.st

# Linux/Mac
diff output/20260121_195204/repoeval_readwriteFile/readful_result_before_fix/ReadFile.st \
     output/20260121_195204/repoeval_readwriteFile/readful_result/ReadFile.st
```

## 🚀 评估脚本更新

由于不再有 `_fixed` 目录，评估脚本需要更新：

### evaluate_output.py

```bash
# 之前
python evaluate_output.py --dir output/20260121_195204_fixed

# 现在
python evaluate_output.py --dir output/20260121_195204
```

### evaluate_single_project.py

```bash
# 之前
python evaluate_single_project.py output/20260121_195204_fixed/repoeval_readwriteFile

# 现在
python evaluate_single_project.py output/20260121_195204/repoeval_readwriteFile
```

## ⚠️ 注意事项

1. **备份会被覆盖**：每次运行修复时，旧的 `readful_result_before_fix` 会被删除并重新创建
2. **历史记录累积**：`readful_result_history` 会持续累积，不会自动清理
3. **兼容性**：旧的 `in_place=False` 模式仍然保留，如需使用旧模式可手动修改代码

## 📚 相关文件

- `full_process.py`: 主流程脚本（已修改）
- `generator/process_generations.py`: 生成阶段（支持 `readful_result_no_provide`）
- `evaluate_output.py`: 批量评估脚本（需要更新路径）
- `evaluate_single_project.py`: 单项目评估脚本（需要更新路径）

## 🔄 版本历史

- **2026-01-21 v2**: 实现原地修复模式，不再创建 `_fixed` 目录
- **2026-01-21 v1**: 添加 `readful_result_no_provide` 功能
- **2026-01-20**: 初始版本（两个目录模式）


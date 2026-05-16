# ReadFul Result No Provide 功能说明

## 📋 功能概述

在生成 `readful_result` 目录的同时，自动创建 `readful_result_no_provide` 目录，包含去除了 `provide_code`（定义部分）的 ST 文件。

## 🎯 用途

- **对比分析**: 方便对比生成的代码实现部分和完整代码的差异
- **代码评估**: 可以单独评估模型生成的实现部分质量，排除定义部分的干扰
- **代码提取**: 快速获取纯实现逻辑，用于后续分析或重组

## 📁 目录结构

生成结果会包含两个目录：

```
output/[timestamp]_fixed/[project_name]/
├── readful_result/              # 完整版本（包含 provide_code）
│   ├── ReadFile.st              # FUNCTION_BLOCK 声明 + VAR 定义 + 实现逻辑
│   └── WriteFile.st
└── readful_result_no_provide/   # 精简版本（仅实现逻辑）
    ├── ReadFile.st              # 仅包含实现逻辑部分
    └── WriteFile.st
```

## 📊 内容对比示例

### readful_result/ReadFile.st（完整版本）
```st
FUNCTION_BLOCK ReadFile          ← provide_code 开始
VAR_INPUT
    bExec    :    BOOL;
    fileName :    STRING;
END_VAR
VAR
    nState   :    BYTE;
    ...
END_VAR
VAR_OUTPUT
    ReadBuffer : ARRAY[0..255] OF BYTE;
    ...
END_VAR                          ← provide_code 结束

// 实现逻辑
fbRtrig(CLK := bExec);
IF fbRtrig.Q THEN
    nState := 1;
END_IF;
...
END_FUNCTION_BLOCK
```

### readful_result_no_provide/ReadFile.st（精简版本）
```st
// 实现逻辑
fbRtrig(CLK := bExec);
IF fbRtrig.Q THEN
    nState := 1;
END_IF;
...
END_FUNCTION_BLOCK
```

## 🔧 实现原理

1. **生成阶段**（`full_process.py` → `process_generations.py`）
   - 调用 `process_project()` 生成 `readful_result` 目录（包含 `provide_code`）

2. **修复阶段**（`full_process.py` → `run_fix()`）
   - 修复 `readful_result` 中的代码
   - 修复完成后，调用 `create_no_provide_version()` 函数
   - 从修复后的 `readful_result` 中去除 `provide_code`，生成 `readful_result_no_provide`

3. **去除 provide_code 的逻辑**
   - 读取 `dataset/query/[project_name]/[function_name].json` 获取 `provide_code`
   - 从修复后的 ST 文件开头移除 `provide_code` 部分
   - 保存到 `readful_result_no_provide` 目录

4. **代码修改位置**
   - `full_process.py`: 添加 `create_no_provide_version()` 函数
   - `full_process.py`: 在 `run_fix()` 结束前调用该函数

## ✅ 启用状态

**当前已默认启用**，运行 `full_process.py` 时会在修复后自动生成：

```bash
python full_process.py --project readwriteFile
```

输出示例：
```
================================================================================
开始验证和修复: repoeval_readwriteFile
================================================================================
  ✓ 已备份原始 readful_result 到 readful_result_before_fix
  找到 2 个ST文件

  处理文件: ReadFile.st
    开始自动修复...
    ✓ 修复成功！共尝试 2 次

  ✓ 修复完成: 2/2 个文件修复成功

  生成不含 provide_code 的版本...
  ✓ 已生成 readful_result_no_provide 目录，包含 2 个 ST 文件（修复后，去除 provide_code）
```

## 💡 使用场景

### 1. 代码质量评估
对比 `readful_result_no_provide` 与 ground truth 的实现部分，排除定义干扰。

### 2. 代码差异分析
```bash
# 对比完整版本
diff output/.../readful_result/ReadFile.st \
     real_ground_truth/.../readful_result/ReadFile.st

# 对比精简版本（仅实现逻辑）
diff output/.../readful_result_no_provide/ReadFile.st \
     dataset/generation_context_ground_truth/.../ReadFile.st
```

### 3. CodeBLEU 评估
未来可以添加针对 `readful_result_no_provide` 的单独评估脚本，专门评估实现逻辑的质量。

## 🚀 扩展建议

如果需要针对 `readful_result_no_provide` 进行 CodeBLEU 评估，可以创建类似 `evaluate_no_provide.py` 的脚本：

```python
# 示例：评估不含 provide_code 的版本
evaluate_and_save(
    project_dir,
    readful_result_subdir="readful_result_no_provide",  # 使用精简版本
    ground_truth_subdir="generation_context_ground_truth",
    output_filename="codebleu_evaluation_no_provide.json"
)
```

## 📝 注意事项

1. **两个目录独立**: `readful_result` 和 `readful_result_no_provide` 互不影响
2. **同步生成**: 两个目录会在同一时间生成，确保一致性
3. **文件数量相同**: 两个目录包含相同的文件列表，仅内容不同
4. **不影响现有流程**: 现有的评估、修复流程仍然使用 `readful_result`

## 🔄 版本历史

- **2026-01-21**: 功能添加并默认启用
  - 修改 `generator/process_generations.py`
  - 修改 `full_process.py`
  - 自动生成 `readful_result_no_provide` 目录


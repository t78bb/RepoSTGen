# 编译通过率测试脚本

## 功能说明

`test_compile_rate.py` 用于测试 ST 代码的编译通过率，**不进行代码修复**，只统计编译结果。

### 测试目录

- **output 目录**：测试 `readful_result` 子目录（生成的代码）
- **ground truth 目录**：测试 `full_result` 子目录（包含完整定义的代码）

### 测试标准

- **编译通过**：返回结果中 `Errors` 字段为空（或 `success=True`）
- **编译失败**：返回结果中包含错误信息

## 使用方法

### 基本用法

#### 1. 测试 output 目录下的指定子目录

```bash
python analysis_script/compile_test/test_compile_rate.py --output-dir output/20260123_171908
```

#### 2. 测试 ground truth 目录

```bash
python analysis_script/compile_test/test_compile_rate.py --gt-dir real_groud_truth最新
```

#### 3. 同时测试两个目录

```bash
python analysis_script/compile_test/test_compile_rate.py \
    --output-dir output/20260123_171908 \
    --gt-dir real_groud_truth最新
```

### 完整参数

```bash
python analysis_script/compile_test/test_compile_rate.py \
    --output-dir <output子目录> \          # 可选：output 目录下的子目录
    --gt-dir <ground_truth目录> \          # 可选：ground truth 目录（默认：real_groud_truth最新）
    --ip-port <API地址> \                  # 可选：CODESYS API 地址（默认使用环境变量）
    --output <输出文件路径>                 # 可选：输出 JSON 文件路径（默认自动生成）
```

### 环境变量

- `CODESYS_API_URL`: CODESYS API 地址（默认：`http://192.168.103.117:9000/api/v1/pou/project_workflow`）

## 输出结果

### JSON 文件结构

```json
{
  "test_time": "20260124_164300",
  "output_results": [
    {
      "directory": "output/20260123_171908/repoeval_counter",
      "project_name": "repoeval_counter",
      "files": [
        {
          "file_path": "...",
          "file_name": "FB_counter.st",
          "block_name": "FB_counter",
          "project_name": "repoeval_counter",
          "passed": true,
          "success": true,
          "errors_count": 0,
          "errors": []
        }
      ],
      "total_files": 1,
      "passed_files": 1,
      "failed_files": 0,
      "pass_rate": 100.0
    }
  ],
  "ground_truth_results": [
    {
      "directory": "real_groud_truth最新/repoeval_counter",
      "project_name": "repoeval_counter",
      "files": [...],
      "total_files": 1,
      "passed_files": 1,
      "failed_files": 0,
      "pass_rate": 100.0
    }
  ],
  "summary": {
    "total_projects": 2,
    "total_files": 2,
    "total_passed_files": 2,
    "total_failed_files": 0,
    "overall_pass_rate": 100.0
  }
}
```

### 结果说明

- **`passed`**: 是否编译通过（`Errors` 字段为空）
- **`success`**: API 调用是否成功
- **`errors_count`**: 错误数量
- **`errors`**: 详细错误信息列表
- **`pass_rate`**: 项目级别的编译通过率（百分比）
- **`overall_pass_rate`**: 总体编译通过率（百分比）

## 输出文件位置

默认情况下，结果文件保存在脚本同目录下，文件名格式：
```
compile_test_result_YYYYMMDD_HHMMSS.json
```

可以通过 `--output` 参数指定自定义路径。

## 注意事项

1. **不进行代码修复**：脚本只测试编译，不会修改任何代码
2. **需要 CODESYS API 服务**：确保 API 服务正常运行
3. **测试目录结构**：
   - output 目录：需要包含 `readful_result` 子目录
   - ground truth 目录：需要包含 `full_result` 子目录
4. **文件格式**：只测试 `.st` 文件

## 辅助脚本

### create_full_result.py

用于为 ground truth 文件添加完整的定义部分和结束标记，生成 `full_result` 目录。

#### 功能
- 从 `dataset/BEIR_data/[项目名]/queries.jsonl` 中提取函数定义
- 将定义部分与 `readful_result` 中的实现部分合并
- 自动检测 POU 类型（FUNCTION、FUNCTION_BLOCK、METHOD）
- 添加对应的结束标记（END_FUNCTION、END_FUNCTION_BLOCK、END_METHOD）
- 结果保存在 `full_result` 子目录中

#### 使用方法
```bash
python analysis_script/compile_test/create_full_result.py
```

该脚本会自动处理 `real_groud_truth最新` 目录下所有包含 `readful_result` 的项目。

#### 输出结构
```
real_groud_truth最新/
├── repoeval_project1/
│   ├── readful_result/          # 原始实现代码（不含定义）
│   │   └── Function1.st
│   └── full_result/             # 完整代码（包含定义和结束标记）
│       └── Function1.st
```



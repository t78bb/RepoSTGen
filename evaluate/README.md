# CodeBLEU 评估模块

## 功能说明

此模块用于评估生成的 ST 代码与参考代码的相似度，使用 CodeBLEU 指标进行评估。

## 评估指标

CodeBLEU 综合了以下四个维度：

1. **N-gram 匹配** - 词法相似度
2. **加权 N-gram 匹配** - 考虑关键词权重的词法相似度
3. **语法树匹配** - AST 结构相似度
4. **数据流匹配** - 变量依赖关系相似度

## 使用方法

### 1. 集成在完整流程中（推荐）

在 `full_process.py` 中自动执行，修复完成后会自动进行评估：

```bash
python full_process.py --project three-axis_CNC_motion
```

如果不想执行评估，可以跳过：

```bash
python full_process.py --project three-axis_CNC_motion --skip_evaluate
```

### 2. 单独评估某个项目

对已经生成和修复完成的项目进行评估：

```bash
python evaluate/codebleu_evaluator.py "output/20260120_205101_fixed/repoeval_three-axis_CNC_motion"
```

带参数：

```bash
python evaluate/codebleu_evaluator.py \
    "output/20260120_205101_fixed/repoeval_three-axis_CNC_motion" \
    --lang python \
    --output my_evaluation.json
```

### 3. 在代码中调用

```python
from evaluate import evaluate_and_save
from pathlib import Path

project_dir = Path("output/20260120_205101_fixed/repoeval_three-axis_CNC_motion")
success = evaluate_and_save(
    project_dir,
    output_filename="codebleu_evaluation.json",
    lang="python"  # ST 代码使用 python 作为近似
)
```

## 输入要求

评估需要以下文件：

- `readful_result/*.st` - 生成的 ST 代码文件
- 参考文件位于 `dataset/generation_context_ground_truth/[项目名]/*.st`

## 输出格式

评估结果保存为 JSON 文件（默认：`codebleu_evaluation.json`），格式如下：

```json
{
  "project_name": "repoeval_three-axis_CNC_motion",
  "num_cases": 5,
  "language": "python",
  "weights": [0.25, 0.25, 0.25, 0.25],
  "average_scores": {
    "codebleu": 0.6543,
    "ngram_match_score": 0.5234,
    "weighted_ngram_match_score": 0.5678,
    "syntax_match_score": 0.7890,
    "dataflow_match_score": 0.7321
  },
  "case_results": [
    {
      "case_id": 0,
      "codebleu": 0.6234,
      "ngram_match_score": 0.5123,
      "weighted_ngram_match_score": 0.5456,
      "syntax_match_score": 0.7654,
      "dataflow_match_score": 0.7123,
      "reference_length": 1234,
      "prediction_length": 1456
    },
    ...
  ]
}
```

## 注意事项

1. **ST 语言支持**：CodeBLEU 原生不支持 ST (Structured Text) 语言，当前使用 Python 解析器作为近似评估
2. **依赖要求**：需要安装 `tree-sitter` 和 `tree-sitter-python`
3. **评估时间**：大型项目评估可能需要几分钟时间

## 安装依赖

```bash
pip install "tree-sitter>=0.22.0,<0.24.0" "tree-sitter-python~=0.21"
```

## 示例输出

```
📊 开始评估: repoeval_three-axis_CNC_motion
================================================================================
  📊 找到 3 个样本，开始评估...
    Case 1/3: CodeBLEU=0.6234
    Case 2/3: CodeBLEU=0.7123
    Case 3/3: CodeBLEU=0.5678

  ✅ 评估完成:
     平均 CodeBLEU: 0.6345
     N-gram 匹配:   0.5234
     语法树匹配:    0.7123
     数据流匹配:    0.6890
  💾 评估结果已保存到: codebleu_evaluation.json
```

## 分数解读

- **0.8 - 1.0**：非常相似，代码质量优秀
- **0.6 - 0.8**：较为相似，代码质量良好
- **0.4 - 0.6**：部分相似，代码需要改进
- **< 0.4**：差异较大，代码质量较差


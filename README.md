# figshare 发布版（代码包）

此目录用于上传到 figshare 的**纯代码**发布包，已（或将）从仓库中筛选拷贝得到：

- **包含**：完整流程脚本、LLM 生成与评测相关代码、必要的配置/说明文档
- **不包含**：实验输出结果（如 `output/`）、本地环境与敏感信息（如 `myenv/`、根目录 `env` 文件、`.env` 等）、缓存文件（如 `__pycache__/`）

## 目录说明（拷贝自仓库的子模块）

- `generator/`：生成与评测主流程
- `evaluate/`：指标计算（如 CodeBLEU 等）
- `LITL/`：LLM-in-the-loop 评测/汇总相关
- `dataset/`：数据集处理脚本（仅脚本/说明，不含大体量数据文件夹）
- `verifier/`：静态检查/修复相关
- `retrieve/`：检索相关
- `planner/`：规划/上下文窗口相关
- `analysis_script/`：分析脚本
- `codesys_library_construction/`：库构建/抓取脚本（如需要）
- `tree-sitter-structured-text-main/`、`codebleu-main/`、`codebleu/`：评测依赖的第三方或内置实现（如需要）

## 复现提示

请在上传 figshare 前确认：

- 已从 `figshare/` 中排除 `output/`、`myenv/`、`env`、`.env*` 等敏感/无关内容
- 如需同时发布数据集，请**单独**上传数据文件（避免和代码包混在一起）


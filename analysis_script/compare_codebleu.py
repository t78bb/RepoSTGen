import json
import os

# 固定文件路径（baseline和待对比文件）
BASELINE_PATH = r"F:\项目级st补全\repo_gen_project\real_groud_truth最新\evaluation_summary_20260123_160251.json"
# 请在这里替换为第二个待对比文件的路径
COMPARE_PATH = r"F:\项目级st补全\repo_gen_project\output\20260302_204453\evaluation_summary_20260302_205125.json"

# 需要对比的5个核心指标
METRICS = [
    "codebleu",
    "ngram_match_score",
    "weighted_ngram_match_score",
    "syntax_match_score",
    "dataflow_match_score"
]

def load_json_file(file_path):
    """加载JSON文件，包含异常处理"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON文件解析失败 {file_path}: {str(e)}")
    except Exception as e:
        raise Exception(f"读取文件失败 {file_path}: {str(e)}")

def calculate_diff(baseline_val, compare_val):
    """计算两个值的差值和变化率"""
    if baseline_val == 0:
        diff_rate = 0.0 if compare_val == 0 else float('inf')
    else:
        diff_rate = ((compare_val - baseline_val) / baseline_val) * 100
    diff = compare_val - baseline_val
    return diff, diff_rate

def print_aligned_results():
    """打印对齐的对比结果"""
    try:
        # 加载两个文件
        baseline_data = load_json_file(BASELINE_PATH)
        compare_data = load_json_file(COMPARE_PATH)
        
        # 1. 打印整体统计对比（overall_statistics）
        print("=" * 120)
        print(f"{'整体统计对比':^120}")
        print("=" * 120)
        # 打印表头
        header = (
            f"{'指标名称':<30} | {'Baseline值':<15} | {'对比值':<15} | {'差值':<15} | {'变化率(%)':<15}"
        )
        print(header)
        print("-" * 120)
        
        # 遍历指标打印整体统计
        baseline_overall = baseline_data["overall_statistics"]["average_scores"]
        compare_overall = compare_data["overall_statistics"]["average_scores"]
        
        for metric in METRICS:
            b_val = baseline_overall.get(metric, 0.0)
            c_val = compare_overall.get(metric, 0.0)
            diff, diff_rate = calculate_diff(b_val, c_val)
            
            # 格式化输出（保留8位小数，对齐）
            line = (
                f"{metric:<30} | {b_val:<15.8f} | {c_val:<15.8f} | "
                f"{diff:<15.8f} | {diff_rate:<15.2f}"
            )
            print(line)
        
        # 2. 打印各项目详细对比
        print("\n" + "=" * 120)
        print(f"{'各项目详细对比':^120}")
        print("=" * 120)
        
        # 获取所有项目列表（合并两个文件的项目）
        all_projects = set(baseline_data["project_statistics"].keys()) | set(compare_data["project_statistics"].keys())
        
        for project in sorted(all_projects):
            print(f"\n【项目】: {project}")
            print("-" * 110)
            print(f"{'指标名称':<30} | {'Baseline值':<15} | {'对比值':<15} | {'差值':<15} | {'变化率(%)':<15}")
            print("-" * 110)
            
            # 获取该项目的分数
            baseline_proj = baseline_data["project_statistics"].get(project, {})
            compare_proj = compare_data["project_statistics"].get(project, {})
            
            b_scores = baseline_proj.get("average_scores", {}) if baseline_proj else {}
            c_scores = compare_proj.get("average_scores", {}) if compare_proj else {}
            
            for metric in METRICS:
                b_val = b_scores.get(metric, 0.0)
                c_val = c_scores.get(metric, 0.0)
                diff, diff_rate = calculate_diff(b_val, c_val)
                
                line = (
                    f"{metric:<30} | {b_val:<15.8f} | {c_val:<15.8f} | "
                    f"{diff:<15.8f} | {diff_rate:<15.2f}"
                )
                print(line)
        
        print("\n" + "=" * 120)
        print(f"{'对比完成':^120}")
        print("=" * 120)
        
    except FileNotFoundError as e:
        print(f"错误: {str(e)}")
    except KeyError as e:
        print(f"错误: JSON文件结构异常，缺少字段 {str(e)}")
    except Exception as e:
        print(f"程序执行错误: {str(e)}")

if __name__ == "__main__":
    # 执行对比并打印结果
    print_aligned_results()
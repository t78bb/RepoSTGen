import json
import argparse
from pathlib import Path

def extract_metrics(json_file: Path) -> None:
    """
    从JSON文件的project_summary字段中提取每个项目的average_overall_score和通过率(passed_cases/total_cases)
    
    Args:
        json_file: 待处理的JSON文件路径
    """
    # 检查文件是否存在
    if not json_file.exists():
        print(f"错误：文件 {json_file} 不存在！")
        return
    
    # 读取并解析JSON文件
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"错误：文件 {json_file} 不是有效的JSON格式！")
        return
    except Exception as e:
        print(f"读取文件时发生错误：{str(e)}")
        return
    
    # 只处理project_summary字段下的数据
    project_summary = data.get('project_summary', {})
    if not project_summary:
        print("警告：JSON文件中未找到project_summary字段，或该字段为空！")
        return
    
    # 遍历每个项目并提取指标
    print(f"{'项目名称':<30} {'平均总分':<10} {'通过率(%)':<10}")
    print("-" * 60)
    for project_name, project_data in project_summary.items():
        # 提取平均总分
        avg_score = project_data.get('average_overall_score', 'N/A')
        
        # 计算通过率
        total_cases = project_data.get('total_cases', 0)
        passed_cases = project_data.get('passed_cases', 0)
        
        if total_cases == 0:
            pass_rate = "0.00"
        else:
            pass_rate = f"{(passed_cases / total_cases) * 100:.2f}"
        
        # 格式化输出
        print(f"{project_name:<30} {avg_score:<10} {pass_rate:<10}")

if __name__ == "__main__":
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='提取JSON文件project_summary中的测试指标（平均总分、通过率）')
    parser.add_argument('file_path', type=str, help='待处理的JSON文件路径（如：./test_result.json）')
    args = parser.parse_args()
    
    # 调用提取函数
    extract_metrics(Path(args.file_path))
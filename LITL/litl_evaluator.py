#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LITL (LLM-in-the-Loop) 验证主程序

使用独立的验证器LLM自动评估生成器LLM生成的IEC 61131-3代码
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import traceback

# 添加项目根目录到Python路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    import config
    from evaluation_prompt import get_evaluation_prompt, get_system_prompt
except ImportError as e:
    print(f"错误: 无法导入必要的模块: {e}")
    sys.exit(1)

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    try:
        import openai
        OPENAI_AVAILABLE = True
        OPENAI_V0 = True  # 使用旧版本API
    except ImportError:
        print("错误: 请先安装 openai 库: pip install openai")
        sys.exit(1)
        OPENAI_AVAILABLE = False
        OPENAI_V0 = False


class LITLEvaluator:
    """LITL评估器类"""
    
    def __init__(self, api_key: str = None, api_base: str = None, model: str = None):
        """
        初始化评估器
        
        参数:
            api_key: OpenAI API密钥
            api_base: API基础URL（可选）
            model: 模型名称
        """
        self.api_key = api_key or config.API_KEY
        self.api_base = api_base or config.API_BASE
        self.model = model or config.MODEL_NAME
        
        if not self.api_key:
            raise ValueError("未设置API密钥！请在config.py中设置或通过环境变量OPENAI_API_KEY设置")
        
        # 配置OpenAI客户端（支持新版本和旧版本）
        try:
            # 尝试使用新版本API (v1.0+)
            if 'OpenAI' in globals():
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.api_base if self.api_base else None
                )
                self.use_v1_api = True
            else:
                raise ImportError("OpenAI class not available")
        except (ImportError, TypeError, AttributeError, NameError):
            # 回退到旧版本API (v0.x)
            print("back to old version")
            import openai
            openai.api_key = self.api_key
            if self.api_base and self.api_base != "https://api.openai.com/v1":
                openai.api_base = self.api_base
            self.client = openai
            self.use_v1_api = False
        
        self.results = []
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "passed": 0,
            "not_passed": 0,
            "errors": 0
        }
        # 当前评测目录的实际路径（用于写入结果文件）
        self.eval_directory = None
    
    def evaluate_code(self, requirement: str, ground_truth: str, 
                      generated_code: str, case_name: str, project_name: str,
                      requirement_path: str = None, ground_truth_path: str = None,
                      generated_code_path: str = None) -> Dict:
        """
        评估单个代码用例
        
        参数:
            requirement: 任务规范
            ground_truth: 参考代码
            generated_code: 生成的代码
            case_name: 用例名称
            project_name: 项目名称
            requirement_path: 任务规范文件路径（可选）
            ground_truth_path: 参考代码文件路径（可选）
            generated_code_path: 生成代码文件路径（可选）
        
        返回:
            评估结果字典
        """
        try:
            # 构建评估提示
            prompt = get_evaluation_prompt(
                requirement, ground_truth, generated_code,
                requirement_path=requirement_path,
                ground_truth_path=ground_truth_path,
                generated_code_path=generated_code_path
            )
            system_prompt = get_system_prompt()
            
            # 调用LLM API
            if config.DEBUG:
                print(f"\n调试: 正在调用API评估 {project_name}/{case_name}")
            
            response = self._call_api(system_prompt, prompt)
            
            # 解析响应
            result = self._parse_response(response, case_name, project_name)
            
            return result
            
        except Exception as e:
            error_msg = f"评估失败: {str(e)}"
            if config.DEBUG:
                error_msg += f"\n{traceback.format_exc()}"
            
            return {
                "case_name": case_name,
                "project_name": project_name,
                "status": "error",
                "error": error_msg,
                "scores": None,
                "overall_score": 0.0,
                "assessment": "ERROR",
                "key_findings": error_msg
            }
    
    def _call_api(self, system_prompt: str, user_prompt: str, retry_count: int = 0) -> str:
        """
        调用LLM API
        
        参数:
            system_prompt: 系统提示
            user_prompt: 用户提示
            retry_count: 当前重试次数
        
        返回:
            API响应文本
        """
        try:
            if self.use_v1_api:
                # 使用新版本API (v1.0+)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.0,  # 使用确定性输出
                    timeout=config.API_TIMEOUT
                )
                return response.choices[0].message.content.strip()
            else:
                # 使用旧版本API (v0.x)
                response = self.client.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.0,  # 使用确定性输出
                    timeout=config.API_TIMEOUT
                )
                return response.choices[0].message.content.strip()
            
        except Exception as e:
            error_msg = str(e)
            error_type = type(e).__name__
            print(error_msg)
            # 提供更详细的错误信息
            if retry_count == 0 and config.DEBUG:
                print(f"\n  调试信息: {error_type}: {error_msg}")
            
            if retry_count < config.MAX_RETRIES:
                wait_time = 2 ** retry_count  # 指数退避
                print(f"  API调用失败，{wait_time}秒后重试... ({retry_count + 1}/{config.MAX_RETRIES})")
                if config.DEBUG:
                    print(f"  错误详情: {error_type}: {error_msg[:200]}")
                time.sleep(wait_time)
                return self._call_api(system_prompt, user_prompt, retry_count + 1)
            else:
                # 最后一次重试失败，抛出详细错误
                raise Exception(f"API调用失败（已重试{config.MAX_RETRIES}次）: {error_type}: {error_msg}")
    
    def _parse_response(self, response: str, case_name: str, project_name: str) -> Dict:
        """
        解析LLM响应
        
        参数:
            response: LLM响应文本
            case_name: 用例名称
            project_name: 项目名称
        
        返回:
            解析后的结果字典
        """
        # 尝试提取JSON部分
        response = response.strip()
        
        # 移除可能的markdown代码块标记
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        
        response = response.strip()
        
        # 解析JSON
        try:
            data = json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"无法解析JSON响应: {str(e)}\n响应内容: {response[:200]}...")
        
        # 验证必要字段
        required_fields = ["scores", "justifications", "overall_assessment", "key_findings"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"响应缺少必要字段: {field}")
        
        # 计算综合得分
        scores = data["scores"]
        overall_score = 0.0
        for dimension, weight_info in config.EVALUATION_DIMENSIONS.items():
            if dimension not in scores:
                raise ValueError(f"评分缺少维度: {dimension}")
            score = float(scores[dimension])
            weight = weight_info["weight"]
            overall_score += score * weight
        
        # 判断是否通过（基于综合得分，这是客观标准）
        passed = overall_score >= config.PASS_THRESHOLD
        
        # 统一assessment字段：基于程序计算的passed值，而不是LLM的主观判断
        # 这样可以确保assessment和passed字段一致
        assessment = "PASS" if passed else "FAIL"
        
        # 如果LLM的assessment与程序计算不一致，记录LLM的原始判断作为参考
        llm_assessment = data.get("overall_assessment", assessment)
        if llm_assessment.upper() != assessment:
            # LLM的判断与程序计算不一致，在key_findings中说明
            if "key_findings" in data:
                data["key_findings"] += f" [注意：LLM主观判断为{llm_assessment}，但基于综合得分{overall_score:.2f}，客观评估为{assessment}]"
        
        return {
            "case_name": case_name,
            "project_name": project_name,
            "status": "success",
            "scores": scores,
            "justifications": data["justifications"],
            "overall_score": round(overall_score, 2),
            "assessment": assessment,  # 使用程序计算的assessment，确保与passed一致
            "llm_assessment": llm_assessment,  # 保留LLM的原始判断作为参考
            "passed": passed,
            "key_findings": data["key_findings"]
        }
    
    def evaluate_directory(self, target_dir: str) -> List[Dict]:
        """
        评估指定目录下的所有项目
        
        参数:
            target_dir: 目标目录名称
                - 如果在output下存在，使用 output/target_dir
                - 如果在项目根目录下存在，使用项目根目录/target_dir
                - 例如: "0130版本_无planner目前sota" 或 "real_groud_truth最新"
        
        返回:
            所有评估结果的列表
        """
        if target_dir is None:
            raise ValueError("必须指定 --dir 参数（目录名称）")
        
        # 首先尝试在output目录下查找
        output_path = config.OUTPUT_BASE_DIR / target_dir
        # 然后尝试在项目根目录下查找
        root_path = config.REPO_ROOT / target_dir
        
        # 确定使用哪个路径
        if output_path.exists():
            output_dir = output_path
            print(f"📁 在output目录下找到: {output_dir}")
        elif root_path.exists():
            output_dir = root_path
            print(f"📁 在项目根目录下找到: {output_dir}")
        else:
            raise ValueError(
                f"目录不存在: {target_dir}\n"
                f"  已检查: {output_path}\n"
                f"  已检查: {root_path}"
            )
        
        if not output_dir.exists():
            raise ValueError(f"目标目录不存在: {output_dir}")
        
        # 记录实际评测目录路径，便于在结果文件中展示
        self.eval_directory = str(output_dir.resolve())
        
        print(f"\n开始LITL评估")
        print(f"目标目录: {output_dir}")
        print(f"验证器模型: {self.model}")
        print("=" * 80)
        
        # 遍历所有项目目录
        project_dirs = [d for d in output_dir.iterdir() if d.is_dir()]
        
        for project_dir in sorted(project_dirs):
            project_name = project_dir.name
            print(f"\n处理项目: {project_name}")
            
            # 检查readful_result目录
            readful_result_dir = project_dir / "readful_result"
            if not readful_result_dir.exists():
                print(f"  ⚠️  跳过（无readful_result目录）")
                continue
            
            # 获取所有ST文件
            st_files = list(readful_result_dir.glob("*.st"))
            if not st_files:
                print(f"  ⚠️  跳过（readful_result目录为空）")
                continue
            
            print(f"  找到 {len(st_files)} 个用例")
            
            # 评估每个用例
            for st_file in sorted(st_files):
                case_name = st_file.stem  # 文件名（不含扩展名）
                self._evaluate_case(project_name, case_name, st_file)
        
        return self.results
    
    @staticmethod
    def remove_last_line(code: str) -> str:
        """
        去掉代码文本的最后一行（用于 readful_result 读取后的处理）。
        若为空或仅一行，则返回去掉最后一行的结果（可能为空字符串）。
        """
        if not code:
            return code
        lines = code.splitlines(keepends=True)
        if not lines:
            return code
        return "".join(lines[:-1]).rstrip("\n")

    def _evaluate_case(self, project_name: str, case_name: str, generated_file: Path):
        """
        评估单个用例
        
        参数:
            project_name: 项目名称（如 "repoeval_electronic_gear_motion"）
            case_name: 用例名称（如 "FB_DualAxisPower"）
            generated_file: 生成代码文件路径
        """
        self.stats["total"] += 1
        
        print(f"    [{self.stats['total']}] {case_name} ... ", end="", flush=True)
        
        try:
            # 1. 读取生成的代码（去掉最后一行后再参与评估）
            generated_code = generated_file.read_text(encoding='utf-8')
            generated_code = self.remove_last_line(generated_code)
            
            # 2. 找到对应的ground truth
            # 去掉 "repoeval_" 前缀
            dataset_project_name = project_name.replace("repoeval_", "")
            ground_truth_file = config.PROJECT_CODE_DIR / dataset_project_name / "FUN" / f"{case_name}.st"
            
            if not ground_truth_file.exists():
                raise FileNotFoundError(f"找不到ground truth: {ground_truth_file}")
            
            ground_truth = ground_truth_file.read_text(encoding='utf-8')
            
            # 3. 找到对应的requirement
            query_file = config.QUERY_DIR / project_name / f"{case_name}.json"
            
            if not query_file.exists():
                raise FileNotFoundError(f"找不到requirement: {query_file}")
            
            with open(query_file, 'r', encoding='utf-8') as f:
                query_data = json.load(f)
            
            requirement = query_data.get("requirement", "")
            if not requirement:
                raise ValueError(f"requirement字段为空: {query_file}")
            
            # 4. 执行评估
            result = self.evaluate_code(
                requirement=requirement,
                ground_truth=ground_truth,
                generated_code=generated_code,
                case_name=case_name,
                project_name=project_name,
                requirement_path=str(query_file),
                ground_truth_path=str(ground_truth_file),
                generated_code_path=str(generated_file)
            )
            
            # 5. 更新统计
            if result["status"] == "success":
                self.stats["success"] += 1
                if result["passed"]:
                    self.stats["passed"] += 1
                    status_emoji = "✅"
                else:
                    self.stats["not_passed"] += 1
                    status_emoji = "❌"
                print(f"{status_emoji} {result['overall_score']:.1f}/100")
            else:
                self.stats["errors"] += 1
                print(f"⚠️  错误")
            
            # 6. 保存结果
            self.results.append(result)
            
        except Exception as e:
            self.stats["errors"] += 1
            error_msg = str(e)
            if config.DEBUG:
                error_msg += f"\n{traceback.format_exc()}"
            
            print(f"⚠️  异常: {error_msg}")
            
            self.results.append({
                "case_name": case_name,
                "project_name": project_name,
                "status": "error",
                "error": error_msg,
                "scores": None,
                "overall_score": 0.0,
                "assessment": "ERROR",
                "key_findings": error_msg
            })
    
    def save_results(self, output_file: Path = None):
        """
        保存评估结果
        
        参数:
            output_file: 输出文件路径（可选）
        """
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = SCRIPT_DIR / f"litl_evaluation_{timestamp}.json"
        
        # 计算汇总统计信息
        # 1. overall_score的平均值
        overall_scores = []
        for result in self.results:
            if result.get("status") == "success" and "overall_score" in result:
                overall_scores.append(result["overall_score"])
        avg_overall_score = round(sum(overall_scores) / len(overall_scores), 2) if overall_scores else 0.0
        
        # 2. llm_assessment的通过率
        llm_passed_count = 0
        llm_total_count = 0
        for result in self.results:
            if result.get("status") == "success" and "llm_assessment" in result:
                llm_total_count += 1
                if result["llm_assessment"].upper() == "PASS":
                    llm_passed_count += 1
        llm_pass_rate = round(llm_passed_count / llm_total_count * 100, 2) if llm_total_count > 0 else 0.0
        
        # 为每个用例生成简要总览，包含分数和通过情况
        case_overview = []
        for result in self.results:
            overview_item = {
                "project_name": result.get("project_name"),
                "case_name": result.get("case_name"),
                "status": result.get("status"),
            }
            # 对成功评估的用例，补充综合得分和是否通过
            if result.get("status") == "success":
                overview_item["overall_score"] = result.get("overall_score", 0.0)
                overview_item["passed"] = result.get("passed", False)
            else:
                # 失败/异常用例默认视为未通过
                overview_item["overall_score"] = result.get("overall_score", 0.0)
                overview_item["passed"] = False
            case_overview.append(overview_item)

        # 按项目聚合统计：每个 project 的平均得分、通过数量、总 case 数量，
        # 并把所有原始 results 按项目归类
        project_summary = {}
        for result in self.results:
            project_name = result.get("project_name") or "UNKNOWN_PROJECT"
            proj_stats = project_summary.setdefault(project_name, {
                "total_cases": 0,
                "successful": 0,
                "errors": 0,
                "passed_cases": 0,
                # 平均分稍后根据成功用例计算
                "average_overall_score": 0.0,
                # 将该项目下的所有原始 result 放到这里
                "results": [],
                "_score_sum": 0.0,
                "_score_count": 0,
            })

            proj_stats["total_cases"] += 1
            # 存放完整的结果对象，包含 scores/justifications 等全部字段
            proj_stats["results"].append(result)

            if result.get("status") == "success":
                proj_stats["successful"] += 1
                score = float(result.get("overall_score", 0.0))
                proj_stats["_score_sum"] += score
                proj_stats["_score_count"] += 1
                if result.get("llm_assessment", "").upper() == "PASS":
                    proj_stats["passed_cases"] += 1
            else:
                proj_stats["errors"] += 1

        # 计算每个项目的平均综合得分
        for proj_name, proj_stats in project_summary.items():
            if proj_stats["_score_count"] > 0:
                proj_stats["average_overall_score"] = round(
                    proj_stats["_score_sum"] / proj_stats["_score_count"], 2
                )
            else:
                proj_stats["average_overall_score"] = 0.0
            # 删除内部累加字段
            proj_stats.pop("_score_sum", None)
            proj_stats.pop("_score_count", None)

        # 准备输出数据（保持键的插入顺序，使 overview 出现在 results 之前）
        output_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "model": self.model,
                "api_base": self.api_base,
                # 实际评测目录路径
                "eval_directory": self.eval_directory,
                "total_cases": self.stats["total"],
                "successful_evaluations": self.stats["success"],
                "errors": self.stats["errors"],
                "passed": self.stats["passed"],
                "not_passed": self.stats["not_passed"],
                "pass_rate": round(self.stats["passed"] / self.stats["total"] * 100, 2) if self.stats["total"] > 0 else 0,
                # 新增汇总统计
                "average_overall_score": avg_overall_score,
                "llm_assessment_pass_rate": llm_pass_rate,
                "llm_assessment_passed": llm_passed_count,
                "llm_assessment_total": llm_total_count
            },
            "dimensions": config.EVALUATION_DIMENSIONS,
            "pass_threshold": config.PASS_THRESHOLD,
            "project_summary": project_summary
            # "overview": case_overview,
            # "results": self.results
        }
        
        # 保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n结果已保存到: {output_file}")
        
        # 打印统计信息
        print("\n" + "=" * 80)
        print("评估统计")
        print("=" * 80)
        print(f"总用例数:              {self.stats['total']}")
        print(f"成功评估:              {self.stats['success']}")
        print(f"评估失败:              {self.stats['errors']}")
        print(f"通过用例:              {self.stats['passed']}")
        print(f"未通过用例:            {self.stats['not_passed']}")
        if self.stats['total'] > 0:
            print(f"通过率:                {self.stats['passed'] / self.stats['total'] * 100:.2f}%")
        print(f"\n汇总统计:")
        print(f"  平均综合得分:        {avg_overall_score:.2f}/100")
        print(f"  LLM评估通过率:       {llm_pass_rate:.2f}% ({llm_passed_count}/{llm_total_count})")
        print("=" * 80)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="LITL (LLM-in-the-Loop) 代码验证工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 评估output目录下的子目录
  python litl_evaluator.py --dir 0130版本_无planner目前sota
  python litl_evaluator.py --dir 0130版本_无planner目前sota --model gpt-4-turbo
  
  # 评估real_groud_truth最新目录
  python litl_evaluator.py --dir real_groud_truth最新
  
  # 指定输出文件
  python litl_evaluator.py --dir 0130版本_无planner目前sota --output results.json
        """
    )
    
    parser.add_argument(
        "--dir",
        type=str,
        required=True,
        help="要评估的目录名称。例如: '0130版本_无planner目前sota'（在output下）或 'real_groud_truth最新'（在项目根目录下）"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help=f"验证器LLM模型名称（默认: {config.MODEL_NAME}）"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="输出文件路径（默认: litl_evaluation_<timestamp>.json）"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="OpenAI API密钥（也可通过环境变量OPENAI_API_KEY设置）"
    )
    
    parser.add_argument(
        "--api-base",
        type=str,
        default=None,
        help="API基础URL（可选，用于自定义端点）"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="启用调试模式"
    )
    
    args = parser.parse_args()
    
    # 设置调试模式
    if args.debug:
        config.DEBUG = True
    
    try:
        # 创建评估器
        evaluator = LITLEvaluator(
            api_key=args.api_key,
            api_base=args.api_base,
            model=args.model
        )
        
        # 执行评估
        start_time = time.time()
        evaluator.evaluate_directory(args.dir)
        elapsed_time = time.time() - start_time
        
        # 保存结果
        output_file = Path(args.output) if args.output else None
        evaluator.save_results(output_file)
        
        print(f"\n总耗时: {elapsed_time:.1f} 秒")
        
    except KeyboardInterrupt:
        print("\n\n用户中断评估")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        if config.DEBUG:
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


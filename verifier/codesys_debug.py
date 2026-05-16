
import os
import time
import json
import requests
from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class ErrorMessage:
    error_desc: str
    error_type: str
    code_window: Optional[str] = None
    line_no: Optional[int] = None  # 报错所在的行号（相对于源代码的逻辑行号/Path）
    line_content: Optional[str] = None  # 报错所在行的代码内容

    def to_dict(self):
        return {
            "error_desc": self.error_desc,
            "error_type": self.error_type,
            "code_window": self.code_window,
            "line_no": self.line_no,
            "line_content": self.line_content,
        }

    def __str__(self):
        """返回格式化的错误信息字符串"""
        if self.line_no is not None:
            prefix = f"[{self.error_type}] (line {self.line_no}) "
        else:
            prefix = f"[{self.error_type}] "
        result = prefix + self.error_desc
        if self.code_window:
            result += f"\n{self.code_window}"
        return result

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            error_desc=data['error_desc'],
            error_type=data.get('error_type', '代码段错误'),
            code_window=data.get('code_window'),
            line_no=data.get('line_no'),
            line_content=data.get('line_content'),
        )

@dataclass
class ResponseData:
    success: bool
    result: Optional[str] = None
    errors: List[ErrorMessage] = None

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "result": self.result,
            "errors": [e.to_dict() for e in self.errors] if self.errors else []
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict):
        errors = data.get("errors", [])
        return cls(
            success=data["success"],
            result=data.get("result"),
            errors=[ErrorMessage.from_dict(e) for e in errors]
        )

    @classmethod
    def default_false(cls):
        return cls(
            success=False,
            result=None,
            errors=[ErrorMessage(
                error_desc="编译工具调用失败",
                error_type="系统错误"
            )]
        )

class CodesysCompiler:
    def extract_code_window(
        self, source_code: str, error_info: Dict, window_size: int = 3
    ) -> tuple[str, Optional[str]]:
        """
        返回 (代码窗口字符串, 报错所在行内容)。
        报错所在行根据 Path 和 BEGIN/END_VAR 逻辑与原实现保持一致。
        """
        lines = source_code.splitlines()
        path = error_info.get("Path", 0)
        is_def = error_info.get("IsDef", False)

        base_line_idx = 0
        if not is_def:
            begin_idx = next((i for i, line in enumerate(lines) if "BEGIN" in line.upper()), None)
            if begin_idx is not None:
                base_line_idx = begin_idx
            else:
                end_var_indices = [i for i, line in enumerate(lines) if "END_VAR" in line.upper()]
                base_line_idx = end_var_indices[-1] + 1 if end_var_indices else 0

        error_line_idx = base_line_idx + path
        start_idx = max(0, error_line_idx - window_size)
        end_idx = min(len(lines), error_line_idx + window_size + 1)

        window_str = "\n".join(f"{i + 1:>4}: {lines[i]}" for i in range(start_idx, end_idx))
        line_content = lines[error_line_idx] if 0 <= error_line_idx < len(lines) else None
        return window_str, line_content

    def syntax_check(self, project_name: str, block_name: str, st_code: str, ip_port: str) -> ResponseData:
        API_KEY = "admin"  # Default API key, change in production
        # Configure requests session
        print(ip_port)
        print(project_name)
        session = requests.Session()
        session.headers.update({
            'Authorization': 'ApiKey ' + API_KEY,
            'Content-Type': 'application/json'
        })
        URL = ip_port
        print(st_code)
        json_data = {"path": project_name, "BlockName": block_name, "Code": st_code}
        timeout = 80  # Set a reasonable timeout for the request
        try:
            resp = session.post(URL, json=json_data, timeout=timeout)  # Reasonable timeout

            # print(resp.json())
        
            if resp.status_code != 200:
                return ResponseData.default_false()

            raw_data = resp.json()
            raw_errors = [e for e in raw_data.get("Errors", []) if e.get("PouName")]
            # print(json.dumps(raw_errors, ensure_ascii=False), end="")
            simplified_errors = []

            for err in raw_errors:
                code_window, line_content = self.extract_code_window(st_code, err, window_size=3)
                path = err.get("Path", 0)
                simplified_errors.append(ErrorMessage(
                    error_desc=err["ErrorDesc"],
                    error_type="Declaration Section Error" if err.get("IsDef", False) else "Implementation Section Error",
                    code_window=code_window,
                    line_no=path,
                    line_content=line_content,
                ))

            return ResponseData(
                success=raw_data.get("Success", True),
                result=raw_data.get("Result", ""),
                errors=simplified_errors
            )
        except requests.exceptions.ConnectTimeout as e:
            print(f"[Error] Codesys Compiler API 连接超时: {e}")
            print(f"[提示] 无法连接到 {URL}")
            print(f"[提示] 请检查：")
            print(f"  1. Codesys 服务是否在本地主机运行")
            print(f"  2. 是否已建立 SSH 隧道（如果使用内网 IP）")
            print(f"  3. 防火墙是否允许连接")
            print(f"[提示] 查看 CODESYS_SETUP.md 了解详细配置方法")
            return ResponseData.default_false()
        except requests.exceptions.ConnectionError as e:
            print(f"[Error] Codesys Compiler API 连接失败: {e}")
            print(f"[提示] 无法连接到 {URL}")
            print(f"[提示] 请检查网络连接和 API 地址配置")
            return ResponseData.default_false()
        except Exception as e:
            print(f"[Error] Codesys Compiler API failed: {e}")
            print(f"[提示] API 地址: {URL}")
            return ResponseData.default_false()

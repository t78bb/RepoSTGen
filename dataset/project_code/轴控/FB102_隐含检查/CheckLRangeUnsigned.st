// 隐式生成代码:不需要编辑
FUNCTION CheckLRangeUnsigned : ULINT
VAR_INPUT
	value, lower, upper: ULINT;
END_VAR

// 隐式生成代码:只是实现代码的建议
IF (value < lower) THEN
	CheckLRangeUnsigned := lower;
ELSIF(value > upper) THEN
	CheckLRangeUnsigned := upper;
ELSE
	CheckLRangeUnsigned := value;
END_IF
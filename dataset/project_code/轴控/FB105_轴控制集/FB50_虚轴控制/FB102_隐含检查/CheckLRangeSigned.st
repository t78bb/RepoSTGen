// 隐式生成代码:不需要编辑
FUNCTION CheckLRangeSigned : LINT
VAR_INPUT
	value, lower, upper: LINT;
END_VAR

// 隐式生成代码:只是实现代码的建议
IF (value < lower) THEN
	CheckLRangeSigned := lower;
ELSIF(value > upper) THEN
	CheckLRangeSigned := upper;
ELSE
	CheckLRangeSigned := value;
END_IF
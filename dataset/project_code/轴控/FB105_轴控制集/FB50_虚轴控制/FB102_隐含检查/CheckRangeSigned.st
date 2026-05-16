// 隐式生成代码:不需要编辑
FUNCTION CheckRangeSigned : DINT
VAR_INPUT
	value, lower, upper: DINT;
END_VAR

// 隐式生成代码:只是实现代码的建议
IF (value < lower) THEN
	CheckRangeSigned := lower;
ELSIF(value > upper) THEN
	CheckRangeSigned := upper;
ELSE
	CheckRangeSigned := value;
END_IF
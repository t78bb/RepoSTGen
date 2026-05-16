// 隐式生成代码:不需要编辑
FUNCTION CheckRangeUnsigned : UDINT
VAR_INPUT
	value, lower, upper: UDINT;
END_VAR

// 隐式生成代码:只是实现代码的建议
IF (value < lower) THEN
	CheckRangeUnsigned := lower;
ELSIF(value > upper) THEN
	CheckRangeUnsigned := upper;
ELSE
	CheckRangeUnsigned := value;
END_IF
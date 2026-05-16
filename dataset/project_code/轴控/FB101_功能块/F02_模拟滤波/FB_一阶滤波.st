FUNCTION_BLOCK FB_一阶滤波
VAR_INPUT
rInput: REAL:= 0.0; //输入数据
rK: REAL:= 1.0; //增益
tT: TIME; //时间参数
END_VAR
VAR_OUTPUT
rOutput: REAL:= 0.0; //输出数据
END_VAR
VAR
_rT: LREAL;
_rY: LREAL;
END_VAR

IF _rT = 0.0 THEN
    rOutput:= rInput; //输出数据初始化
END_IF
_rT:= TIME_TO_REAL(tT) /10; //10 为 PLC 的采样周期， 单位为 ms

IF ABS(rOutput - rInput) < 1E-6 THEN
    rOutput:= rInput; //防止除零
ELSIF _rT > 0.0 THEN
    rOutput:= (rK / _rT) * rInput + (1.0 - (1.0 / _rT)) * _rY;
ELSE
    rOutput:= rInput; //如果时间常数小于等于零请输出等于输入
END_IF

_rY:= rOutput;

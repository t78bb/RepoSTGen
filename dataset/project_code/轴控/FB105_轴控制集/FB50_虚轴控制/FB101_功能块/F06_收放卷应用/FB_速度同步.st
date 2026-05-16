FUNCTION_BLOCK FB_速度同步
VAR_INPUT
	Enble :BOOL;
    主轴速度 :REAL;
    主轴直径 :REAL;
    主轴减速比 :REAL;
    从轴直径 :REAL;
    从轴减速比 :REAL;
    速度系数 :REAL;
END_VAR
VAR_OUTPUT
	输出角速度: REAL;
END_VAR
VAR
END_VAR

IF Enble THEN
	输出角速度:=速度系数*主轴速度*(主轴直径*从轴减速比/(从轴直径*主轴减速比));
END_IF
FUNCTION_BLOCK FB_锥度计算
VAR_INPUT
   rTensionSet   : REAL;       //张力设定
   rTaper        : REAL;       //锥度系数（1.0）
   rInit_Diameter  : REAL;    //最小卷径
   rAct_Diameter   : REAL;    //实时卷径
END_VAR
VAR_OUTPUT
   rTensionOut   : REAL;     //张力输出
END_VAR
VAR
END_VAR

rTensionOut:=rTensionSet*(1-rTaper*0.01*(1-rInit_Diameter/(rAct_Diameter+0.00001)));
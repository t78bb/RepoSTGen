PROGRAM PLC_PRG
VAR
    rInputValue : REAL;
    nKp : BYTE := 1;
    tTn : TIME := t#1s;
    rOutValue : REAL;
    FB_PT1Filter_0 : FB_PT1Filter;
END_VAR

(* 执行加法运算 *)
rInputValue := rInputValue + 0.5;

(* 调用 PT1 滤波功能块 *)
FB_PT1Filter_0(
    rInput := rInputValue,
    rK := nKp,
    rT := tTn
);

(* 取滤波输出 *)
rOutValue := FB_PT1Filter_0.rOutput;
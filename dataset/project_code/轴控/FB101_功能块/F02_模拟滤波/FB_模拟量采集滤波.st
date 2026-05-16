FUNCTION_BLOCK FB_模拟量采集滤波
VAR_INPUT
    tSampleTime:TIME:=T#200MS; //采样时间
    rInputValue:REAL; //输入数据
END_VAR

VAR_OUTPUT
    rOutputValue:REAL; //输出数据
END_VAR

VAR
    arrBufferData:ARRAY [0..4] OF REAL; //缓存数据
    i:BYTE;
    OverallValue:LREAL;
    fb_SampleTimer:ton;
END_VAR

fb_SampleTimer(IN:= NOT fb_SampleTimer.Q , PT:= tSampleTime);
IF i<5 THEN
   arrBufferData[i]:=rInputValue;
   i:=i+1;
   OverallValue:=arrBufferData[0]+arrBufferData[1]+arrBufferData[2]+arrBufferData[3]+arrBufferData[4];
ELSE
   i:=0;
END_IF

IF fb_SampleTimer.Q THEN
   rOutputValue:=LREAL_TO_REAL(OverallValue/5);
END_IF 
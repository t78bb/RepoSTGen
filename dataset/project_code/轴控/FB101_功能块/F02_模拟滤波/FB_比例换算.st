FUNCTION_BLOCK FB_比例换算
VAR_INPUT
   rIn   :REAL;
   rInMin  :REAL;
   rInMax  :REAL;
   rOutMin  :REAL;
   rOutMax  :REAL;
END_VAR
VAR_OUTPUT
   rOut   :REAL;
END_VAR
VAR
   rK: REAL;
END_VAR

IF rInMax-rInMin<>0  THEN
    rK:=(rOutMax-rOutMin)/(rInMax-rInMin);
END_IF

rOut:=rOutMin+(rIn-rInMin)*rK;
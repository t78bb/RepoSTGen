// 隐式生成代码:不需要编辑
FUNCTION CheckBounds : DINT
VAR_INPUT
	index, lower, upper: DINT;
END_VAR

// 隐式生成代码:只是实现代码的建议
IF  index < lower THEN
	CheckBounds := lower;
ELSIF  index > upper THEN
	CheckBounds := upper;
ELSE  
	CheckBounds := index;
END_IF

(*还可以设置断点,日志信息或其他.比如在异常处停止:
Add CmpApp.library, SysExcept.library and SysTypes2_Itf as newest.
Declaration:
VAR
    _pApp : POINTER TO CmpApp.APPLICATION;
    _result   : SysTypes.RTS_IEC_RESULT;
END_VAR

Implementation:
_pApp := AppGetCurrent(pResult:=_result);
IF  index < lower THEN
        CheckBounds := lower;
        IF _pApp <> 0 THEN
                AppGenerateException(pApp:=_pApp, ulException:=RtsExceptions.RTSEXCPT_ARRAYBOUNDS);
        END_IF
ELSIF  index > upper THEN
        CheckBounds := upper;
        IF _pApp <> 0 THEN
                AppGenerateException(pApp:=_pApp,   ulException:=RtsExceptions.RTSEXCPT_ARRAYBOUNDS);
        END_IF
ELSE  
        CheckBounds := index;
END_IF
*)

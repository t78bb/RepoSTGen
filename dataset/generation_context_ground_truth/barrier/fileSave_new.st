VAR
	lineCount	: INT;
	fileHandle  : DWORD;
	fileName	: STRING;
	fileHandle0 : DWORD;
	datetime	: DATE_AND_TIME;
	UdIntms 	: UDINT;
	UdMsOffset  : UDINT;
	DTimer_Str  : STRING;
	uiYear 		: UINT; 
    uiMonth 	: UINT; 
    uiDay 		: UINT; 
    uiHour 		: UINT; 
    uiMinute 	: UINT; 
    uiSecond 	: UINT;	
	uiMsSecond	: UINT;

	S_Time64		:  SysTime64;
	STT			:  CurTimeEx;
	S_Time			:  SystemTimeDate;
	Time_Str		:  STRING;
	F_err		: DWORD;
	F_HANDL		: DWORD;
END_VAR
VAR_OUTPUT
END_VAR


	STT(SystemTime:= S_Time64, TimeDate:= S_Time);
	Time_Str :='';
	Time_Str := concat(Time_Str,UINT_TO_STRING(S_Time.Year));
	Time_Str := concat(Time_Str,'-');
	Time_Str := concat(Time_Str,UINT_TO_STRING(S_Time.Month));
	Time_Str := concat(Time_Str,'-');
	Time_Str := concat(Time_Str,UINT_TO_STRING(S_Time.Day));
	Time_Str := concat(Time_Str,'_');
	Time_Str := concat(Time_Str,UINT_TO_STRING(S_Time.Hour));
	Time_Str := concat(Time_Str,'-');
	Time_Str := concat(Time_Str,UINT_TO_STRING(S_Time.Minute));
	Time_Str := concat(Time_Str,'-');
	Time_Str := concat(Time_Str,UINT_TO_STRING(S_Time.Second));
	Time_Str := concat(Time_Str,'_');
	Time_Str := concat(Time_Str,UINT_TO_STRING(S_Time.Milliseconds));

	fileName := FilePath;
	fileName := concat(fileName,'/');
	fileName := concat(fileName,devName);

	
	fileName := concat(fileName,'/');
	fileName := concat(fileName,devName);
	fileName := concat(fileName,'-');
	fileName := concat(fileName,Time_Str);
    fileName := concat(fileName,'.txt');

	fileHandle := SysFileOpen(szFile:= fileName, am:=ACCESS_MODE.AM_WRITE, pResult:= ADR(F_err));
	lineCount := -1;
	//fileHandle := SysFileOpen(szFile:= fileName, am:=ACCESS_MODE.AM_APPEND, pResult:= ADR(F_err));
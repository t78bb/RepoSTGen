VAR
	lineCount	: INT;
	fileHandle  : DWORD;
	fileName	: STRING;
	data		: STRING;
	F_err		: DWORD;
	tempInt		: INT;
END_VAR
VAR_OUTPUT
END_VAR

IF fileHandle <> 0 THEN
	lineCount := lineCount + 1;
	tempInt	:= lineCount * intervalt;
	data := INT_TO_STRING(lineCount);
	data := concat(data,'$T$T');
	data := concat(data, INT_TO_STRING(tempInt));
	IF tempInt < 1000 THEN
		data := concat(data,'$T');
	END_IF
	data := concat(data,'$T$T');
	data := concat(data,INT_TO_STRING(positionInt));
	data := concat(data,'$T');
	data := concat(data,INT_TO_STRING(speedInt));
	data := concat(data,'$T');
	data := concat(data,INT_TO_STRING(stateInt));
	data := concat(data,'$R');
	
	SysFileWrite(hFile:=fileHandle , pbyBuffer:= ADR(data) , ulSize:= DINT_TO_DWORD(SysStrLen(data)) , pResult:= ADR(F_err));		// 写入数据

END_IF
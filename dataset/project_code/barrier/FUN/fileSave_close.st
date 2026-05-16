FUNCTION_BLOCK fileSave
VAR_INPUT
	filePath 	:STRING;
	intervalt	:INT;
END_VAR
VAR
	lineCount	: INT;
	fileHandle  : DWORD;
	fileName	: STRING;
END_VAR
VAR_OUTPUT
END_VAR

IF fileHandle <> 0 THEN
	SysFileClose(hFile := fileHandle);
	fileHandle := 0;
END_IF
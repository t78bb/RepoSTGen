FUNCTION_BLOCK fileSave
VAR_INPUT
	filePath 	:STRING;
	devName		: STRING ;
	intervalt	:INT;
END_VAR
VAR
	lineCount	: INT;
	fileHandle  : DWORD;
	fileName	: STRING;
	filePath1	:STRING;
END_VAR
VAR_OUTPUT
END_VAR

filePath1 := FilePath;
filePath1 := concat(filePath1,'/');
filePath1 := concat(filePath1,devName);
SysDirCreate2(filePath1, TRUE);
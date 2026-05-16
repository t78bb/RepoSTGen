PROGRAM PLC_PRG
VAR
	writeBuffer	:	ARRAY[0..255] OF BYTE;//定义写缓冲
	nWriteNum	:	udint;
	nState	:	BYTE;
	i	:	INT;
	fbWriteFile	:	WriteFile;//实例化WriteFile功能块
	fbReadFile	:	ReadFile;
	bWriteFile	:	BOOL;
	readFileName	:	STRING := 'D:/readFile.txt';//读文件的路径
	writeFileName	:	STRING := 'D:/writeFile.txt';//写文件的路径
END_VAR

CASE nState OF 
	0:
		fbReadFile(bExec := FALSE);
		nState := 1;
	1:
		fbReadFile(bExec := TRUE,fileName := readFileName);
		IF fbReadFile.bDone AND NOT fbReadFile.bBusy THEN
			fbReadFile(bExec := FALSE);
			writeBuffer := fbReadFile.ReadBuffer;
			nWriteNum := fbReadFile.nNumRead;
			fbWriteFile(bExec := FALSE);
			nState := 2;
		END_IF
	2:
		fbWriteFile(bExec := TRUE,writeBuffer := writeBuffer,writeNum := nWriteNum,fileName := writeFileName);
		IF fbWriteFile.bDone AND NOT fbWriteFile.bBusy THEN
			fbWriteFile(bExec := FALSE);
			nState := 3;
		END_IF
END_CASE

VAR
	nState	:	BYTE;
	fileHandle	:	UDINT;//文件句柄
	nNumWrite	:	UDINT;//写入文件的字节数
	i	:	BYTE;//定义循环变量
	fbRtrig	:	R_TRIG;//实例化上升沿触发功能块
END_VAR
VAR_OUTPUT
	bDone	:	BOOL;//写入成功
	bBusy	:	BOOL;//写入忙
	bErr	:	BOOL;//写入出错
	nErrId	:	UDINT;//错误代码
END_VAR

CASE nState OF
	0:
		fbRtrig(CLK := bExec);//等待用户触发调用
		IF fbRtrig.Q THEN
			nState := 1;
			bBusy := TRUE;
			bErr := FALSE;
			nErrId := 0;
			bDone := FALSE;
		END_IF
	1:
		//打开文件
		fileHandle := SysFileOpen(szFile := fileName,am := AM_WRITE,pResult := ADR(nErrId));
		IF (fileHandle <> 0) AND (nErrId = 0) THEN
			nState := 2;
		END_IF
		IF nErrId <> 0 THEN
			nState := 0;
			bBusy := FALSE;
			bErr := TRUE; 
		END_IF
	2:
		//写数据到文件
		nNumWrite := SysFileWrite(hFile := fileHandle,pbyBuffer := ADR(writeBuffer),ulSize := writeNum,pResult := ADR(nErrId));
		IF (nNumWrite <> 0) AND (nErrId = 0) THEN
			nState := 3;
		END_IF
		IF nErrId <> 0 THEN
			nState := 0;
			bBusy := FALSE;
			bErr := TRUE; 
		END_IF
	3:
		//关闭文件
		nErrId := SysFileClose(hFile := fileHandle);
		IF nErrId = 0 THEN
			fileHandle := 0;
			nState := 0;
			bBusy := FALSE;
			bDone := TRUE;
		END_IF
		IF nErrId <> 0 THEN
			nState := 0;
			bBusy := FALSE;
			bErr := TRUE; 
		END_IF
END_CASE
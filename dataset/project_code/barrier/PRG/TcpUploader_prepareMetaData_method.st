METHOD prepareMetaData
VAR_INPUT
END_VAR
VAR
	gi				:INT;
	si				:INT;
	
	intTmp			:UINT;	
	pos				:INT;
	byte1			:BYTE;
	byte2			:BYTE;
	plugStat		:BYTE;
	destIp 			:STRING:='172.18.150.31';
	destPort 		:UINT:= 61158;
	tcpConnector	:tcpUpload;
	
	myData 			:ARRAY[1..1024]OF BYTE;
	myDataLen		:__XINT:=21 * 3 + 16;		//总数据长度
	
	init			:BOOL :=TRUE;	
END_VAR

//data head (decimal)
myData[1]	:=	83	;
myData[2]	:=	70	;
myData[3]	:=	68	;
myData[4]	:=	84	;

//data length
myData[5]	:=	0	;
myData[6]	:=	63	;

//healthy data
myData[7]	:=	0	;
myData[8]	:=	11	;

//zero
myData[9]	:=	0	;
myData[10]	:=	0	;
myData[11]	:=	0	;
myData[12]	:=	0	;

myData[13]	:=	0	;
myData[14]	:=	0	;
myData[15]	:=	0	;
myData[16]	:=	0	;

//list
pos := 17;
FOR gi := 1 TO 10 DO
	intTmp := REAL_TO_UINT(gDev.grd[gi].sensor.position * 10);
	byte1 := UINT_TO_BYTE(SHR(intTmp, 8)); 
	byte2 := UINT_TO_BYTE(intTmp AND 255); 
	plugStat := INT_TO_BYTE(gDev.grd[gi].state);
	
	myData[pos] := plugStat;
	pos := pos + 1;		
	myData[pos] := byte1;
	pos := pos + 1;
	myData[pos] := byte2;
	pos := pos + 1;
END_FOR
FOR si := 0 TO 10 DO
	intTmp := REAL_TO_UINT(gDev.sky[si].sensor.position * 10);
	byte1 := UINT_TO_BYTE(SHR(intTmp, 8)); 
	byte2 := UINT_TO_BYTE(intTmp AND 255); 
	plugStat := INT_TO_BYTE(gDev.sky[si].state);
	
	myData[pos] := plugStat;
	pos := pos + 1;		
	myData[pos] := byte1;
	pos := pos + 1;
	myData[pos] := byte2;
	pos := pos + 1;
END_FOR

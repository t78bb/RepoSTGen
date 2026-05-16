PROGRAM TcpUploader
VAR
	destIp 			:STRING:='172.18.150.31';
	destPort 		:UINT:= 61158;
	tcpConnector	:tcpUpload;
	
	myData 			:ARRAY[1..1024]OF BYTE;
	myDataLen		:__XINT:=21 * 3 + 16;		//总数据长度
	
	init			:BOOL :=TRUE;	
END_VAR

//initialize
IF init THEN
	init := FALSE;
	tcpConnector(InetAddress := destIp,port:= destPort);
END_IF

prepareMetaData();

tcpConnector.send(dataLength := myDataLen, sendBuf := myData);

VAR
	tcpConnector	:TCP.Connector;
	tcpStream		:TCP.Stream;
	pointerStream	:POINTER TO TCP.Stream;
	sizeData		:__XINT;

	tcpState		:UINT:=0;
	tcpCount		:UINT:=0;
	
	netState		:INT;
END_VAR

tcpCount := tcpCount + 1;
CASE tcpState OF

	0:			//connet server
		tcpConnector.Connect(sIPAddress:= InetAddress,uiPort:= port,pStream => pointerStream);
		IF pointerStream<>0 THEN
			tcpState :=1;
		ELSE
			tcpState :=2;
		END_IF
		
	1:			
		netState := pointerStream^.Send(ADR(sendBuf),dataLength,diSent=>sizeData);			
		IF netState <> 0 THEN
			tcpState := 2;	
		END_IF
		
		
	2:		 	//断开连接
	    tcpConnector.Disconnect();
		tcpState := 0;

END_CASE
fbReadHoldRegister(
	xExecute	:= TRUE,
	slaveId		:= 1,
	wStartAdr	:= gModbus.srv.request.startAddr,
	wLen		:= gModbus.srv.request.length,
	pTcpStream	:= fbModbusClient.pfbTcpStream,
	modbusHoldRegData:= gModbus.modbusBuffer);
	

IF fbReadHoldRegister.bSucced THEN
	fbReadHoldRegister(xExecute := FALSE,
						modbusHoldRegData:=g_modbusHoldRegData);

	//使用holdingBuff接收供给链控制指令，在下一轮循环中作为服务器保持该数据
	FOR idx := 10 TO 57 DO			//startAddr to startAddr+length-1
		holdingBuff[idx] := gModbus.modbusBuffer[idx];
	END_FOR
	
	iCountAct := 20;		
END_IF

IF fbReadHoldRegister.berror THEN
	fbReadHoldRegister(xExecute :=FALSE,
						modbusHoldRegData:= gModbus.modbusBuffer);
	fbModbusClient.M_Reset();
	connectStatus := 0;
	iCountAct := 10;	
	iErrCode := fbReadHoldRegister.errCode;
END_IF


  
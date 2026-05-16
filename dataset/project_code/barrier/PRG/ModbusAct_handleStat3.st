

fbWriteMutiRegister(
	xExecute	:= TRUE,
	slaveId		:= 1,
	startAddr	:= 250, //gModbus.srv.response.startAddr 110-319
	wRegNum		:= 70,
	value		:= ADR(gModbus.srv.response.data[250]),
	pTcpStream	:= fbModbusClient.pfbTcpStream);
	
IF fbWriteMutiRegister.bSucced THEN
	fbWriteMutiRegister(xExecute := FALSE);
	iCountAct:= 10;
END_IF

IF fbWriteMutiRegister.berror THEN
	fbWriteMutiRegister(xExecute := FALSE);
	fbModbusClient.M_Reset();
	iCountAct := 10;
	connectStatus := 0;
	iErrCode := fbWriteMutiRegister.errCode;
END_IF
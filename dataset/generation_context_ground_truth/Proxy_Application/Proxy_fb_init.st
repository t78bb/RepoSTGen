VAR
	//Pointer to store the reference to the subject being protected
	refToRealSubject : POINTER TO Realsubject;
	//Last value of password entered by the client in the visualization element
	iTempPassword : INT;
END_VAR
VAR_STAT
	//Default password value for the request to be accepted
	iRealPassword : INT := 1234;
END_VAR


//Stores the address of the subject on a field in th Proxy.
THIS^.refToRealSubject := ptrToRealSubject;
//Stores the password value of the client on a field in the Proxy
THIS^.iTempPassword := iTempPassword;

//For security reasons, the Password passed by the client and the Proxi's connection password are compared
IF	THIS^.iTempPassword = THIS^.iRealPassword 
	//If the password sent by the client is correct,
	THEN
	//We verify is the request is a SET or GET request
	IF bReadWrite
		//If the request is a SET request: boolean value TRUE
		THEN
		//The Proxy passes the request to the subject
		THIS^.Set_Method(iSetValue);
		//Once the request is completed, the Proxy responds to the client that the request has been accepted
		PLC_PRG.sTempSetLog := 'Request "SET" accepted';
		//If the request is a GET request: boolean value FALSE
		ELSE
		//The Proxy passes the request to the subject
		PLC_PRG.iGetValueLocal:= THIS^.Get_Method();
		//Once the request is completed, the Proxy responds to the client that the request has been accepted
		PLC_PRG.sTempGetLog := 'Request "GET" accepted';
	END_IF
	
	//If the password sent by the client is incorrect
	ELSE 
	//We verify is the request is a SET or GET request
	IF bReadWrite
		//If the request is a SET request: boolean value TRUE
		THEN
		//The Proxy handles the bad request and response to the client without the subject intervention
		PLC_PRG.sTempSetLog := 'Request denied. Wrong password.';
		//If the request is a GET request: boolean value FALSE
		ELSE
		//The Proxy handles the bad request and response to the client without the subject intervention
		PLC_PRG.sTempGetLog := 'Request denied. Wrong password.';
	END_IF

END_IF
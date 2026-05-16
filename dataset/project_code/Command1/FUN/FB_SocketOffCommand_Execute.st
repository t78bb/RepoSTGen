METHOD Execute
VAR
	refSocket : REFERENCE TO FB_Socket;
END_VAR
IF (__ISVALIDREF(THIS^.refSocket)) THEN
	THIS^.refSocket.On();
END_IF

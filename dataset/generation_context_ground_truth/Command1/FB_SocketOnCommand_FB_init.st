VAR
	refSocket : REFERENCE TO FB_Socket;
END_VAR

IF (__ISVALIDREF(refNewSocket)) THEN
	THIS^.refSocket REF= refNewSocket;
ELSE
	THIS^.refSocket REF= 0;
END_IF
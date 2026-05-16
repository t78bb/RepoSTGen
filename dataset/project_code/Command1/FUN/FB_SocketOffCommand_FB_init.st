FUNCTION_BLOCK PUBLIC FB_AirConStandbyCommand IMPLEMENTS I_Command
VAR
	refSocket : REFERENCE TO FB_Socket;
END_VAR
VAR_INPUT
	bInitRetains : BOOL; // if TRUE, the retain variables are initialized (warm start / cold start)
	bInCopyCode : BOOL;  // if TRUE, the instance afterwards gets moved into the copy code (online change)
	refNewSocket : REFERENCE TO FB_Socket;
END_VAR

IF (__ISVALIDREF(refNewSocket)) THEN
	THIS^.refSocket REF= refNewSocket;
ELSE
	THIS^.refSocket REF= 0;
END_IF

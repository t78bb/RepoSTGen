METHOD FB_init : BOOL
VAR_INPUT
	bInitRetains : BOOL; // if TRUE, the retain variables are initialized (warm start / cold start)
	bInCopyCode : BOOL;  // if TRUE, the instance afterwards gets moved into the copy code (online change)
	refAirConditioning : REFERENCE TO FB_AirConditioning;
END_VAR
VAR
	refAirConditioning : REFERENCE TO FB_AirConditioning;
END_VAR

IF (__ISVALIDREF(refAirConditioning)) THEN
	THIS^.refAirConditioning REF= refAirConditioning;
ELSE
	THIS^.refAirConditioning REF= 0;
END_IF
VAR
	refAirConditioning : REFERENCE TO FB_AirConditioning;
END_VAR


IF (__ISVALIDREF(refAirConditioning)) THEN
	THIS^.refAirConditioning REF= refAirConditioning;
ELSE
	THIS^.refAirConditioning REF= 0;
END_IF

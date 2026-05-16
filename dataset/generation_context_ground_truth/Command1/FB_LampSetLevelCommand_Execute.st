VAR
	refAirConditioning : REFERENCE TO FB_AirConditioning;
END_VAR


IF (__ISVALIDREF(THIS^.refLamp)) THEN
	THIS^.refLamp.SetLevel(THIS^.byNewLevel);
END_IF
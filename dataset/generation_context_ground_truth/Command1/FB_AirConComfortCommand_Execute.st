VAR
	refAirConditioning : REFERENCE TO FB_AirConditioning;
END_VAR

IF (__ISVALIDREF(THIS^.refAirConditioning)) THEN
	THIS^.refAirConditioning.Activate();
	THIS^.refAirConditioning.SetTemperature(20.0);
END_IF

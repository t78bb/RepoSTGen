{attribute 'qualified_only' := ''}
{attribute 'strict' := ''}
TYPE AUTO_SEQUENCE :
(
	///Draining state when system is in auto mode
	DRAINING := 0,
	///Filling state when system is in auto mode
	FILLING := 1,
	///Mixing state when system is in auto mode
	MIXING := 2
);
END_TYPE

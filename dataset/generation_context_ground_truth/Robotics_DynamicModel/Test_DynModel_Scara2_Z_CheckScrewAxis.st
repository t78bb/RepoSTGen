VAR
	state : INT;
	done : BOOL;
	error : BOOL;
	
	axisPos : TRAFO.AXISPOS_REF;
END_VAR
VAR CONSTANT
	EPS : LREAL := 1E-10;
END_VAR

m_dynModel.Init();

WHILE NOT done AND NOT error DO
	CASE state OF
		0:
			axisPos.a0 := 0;	/// [°]
			axisPos.a1 := 0;	/// [°]
			axisPos.a2 := 0;	/// [m]
			
			IF IsScrewAxisAndKinematicEqual(axisPos, EPS) THEN
				state := state + 10;
			ELSE
				error := TRUE;
			END_IF
		
		10:
			axisPos.a0 := 0;	/// [°]
			axisPos.a1 := 90;	/// [°]
			axisPos.a2 := 0.03;	/// [m]
			
			IF IsScrewAxisAndKinematicEqual(axisPos, EPS) THEN
				state := state + 10;
			ELSE
				error := TRUE;
			END_IF
		
		20:
			axisPos.a0 := 45;	/// [°]
			axisPos.a1 := -50;	/// [°]
			axisPos.a2 := -0.01;/// [m]
			
			IF IsScrewAxisAndKinematicEqual(axisPos, EPS) THEN
				state := state + 10;
			ELSE
				error := TRUE;
			END_IF
		
		30:
			done := TRUE;
	END_CASE
END_WHILE

CheckScrewAxis := done AND NOT error;
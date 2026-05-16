FUNCTION_BLOCK FB_时钟脉冲块
(* Function block to simulate a turn signal *)
VAR_INPUT
	ENABLE:BOOL;		(* TRUE:run Blink, FALSE: OUT keeps its value*)
	TIMELOW:TIME;		(* Time for OUT=FALSE *)
	TIMEHIGH:TIME;		(* Time for OUT=TRUE *)
END_VAR
VAR_OUTPUT
	OUT:BOOL;			(* output variable, starting with FALSE *)
END_VAR
VAR
	CLOCK: TP;
END_VAR

CLOCK(IN:= ENABLE, PT:= , Q=> , ET=> );        (* call Timer *)
                                  
IF CLOCK.Q=FALSE AND ENABLE THEN            (* time passed or init *)
    CLOCK(IN:=FALSE);                       (* reset Timer *)
    CLOCK(IN:=TRUE);                        (* restart Timer *)
    IF OUT=FALSE THEN
        CLOCK.PT:=TIMEHIGH;
    ELSE
        CLOCK.PT:=TIMELOW;
    END_IF;
    OUT := NOT OUT;                         (* invert *)
END_IF


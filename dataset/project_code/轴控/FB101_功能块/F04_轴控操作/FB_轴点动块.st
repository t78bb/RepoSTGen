FUNCTION_BLOCK FB_轴点动块
VAR_INPUT
	bForward		:BOOL;
	bBackward	    :BOOL;
	bFast			:BOOL;
	rAcceleration	:REAL:=1000;
	rDeceleration	:REAL:=1000;
	rSlowVelocity	:REAL:=2;
	rFastVelocity	:REAL:=3;
	tiWaitTime		:TIME:=t#0ms;
	rTipDistance	:REAL:=0;
END_VAR
VAR_OUTPUT
	bDone	:BOOL;
	bBusy	:BOOL;
	bCommandAborted	:BOOL;
	bError	:BOOL;
END_VAR
VAR
	diState: DINT;
	MC_MoveRelative_1: MC_MoveRelative;
	T_WaitTime: TON;
	MC_MoveVelocity_1: MC_MoveVelocity;
	MC_Stop_1: MC_Stop;
	bForwardInternal: BOOL;
	bBackwardInternal: BOOL;
	bFastInternal: BOOL;
END_VAR
VAR_IN_OUT
	Axis: SM3_BASIC.AXIS_REF_SM3;
END_VAR

(*
IF NOT V_emergy THEN
	diState	:=100;
END_IF
*)
 
CASE diState OF
	0:	(* Wait for Start *)
		bBusy		:=FALSE;
		bError		:=FALSE;
		bCommandAborted	:=FALSE;
		IF bForward XOR bBackward THEN
			bDone		:=FALSE;
			bBusy		:=TRUE;
			bError		:=FALSE;
			bForwardInternal	:=bForward;
			bBackwardInternal	:=bBackward;
			bFastInternal		:=bFast;
			diState	:=1;
		END_IF

	1:	(* Check parameters - If no Wait time or TippDistance -> immediate move velocity  *)
		IF TIME_TO_DINT(tiWaitTime) = 0 THEN
			diState	:=5;
		ELSIF rTipDistance = 0 THEN
			diState	:=5;
		ELSE
			diState	:=2;
		END_IF

	2:	(* Tipp Distance *)
		IF bForwardInternal AND NOT bBackwardInternal THEN
			MC_MoveRelative_1.Distance		:=rTipDistance;
		ELSIF bBackwardInternal AND NOT bForwardInternal THEN
			MC_MoveRelative_1.Distance		:=rTipDistance * -1;
		ELSE
			bError		:=TRUE;
			diState	:=100;
		END_IF
		IF bFastInternal THEN
			MC_MoveRelative_1.Velocity	:=rFastVelocity;
		ELSE
			MC_MoveRelative_1.Velocity	:=rSlowVelocity;
		END_IF
		MC_MoveRelative_1.Acceleration	:=rAcceleration;
		MC_MoveRelative_1.Deceleration	:=rDeceleration;
		MC_MoveRelative_1(Execute:=TRUE , Distance:= , Velocity:= , Acceleration:= , Deceleration:= , Axis:=Axis , Done=> , CommandAborted=> , Error=> , ErrorID=> );
		diState	:=3;

	3:
		T_WaitTime(IN:=TRUE , PT:=tiWaitTime , Q=> , ET=> );
		MC_MoveRelative_1(Execute:=TRUE , Distance:= , Velocity:= , Acceleration:= , Deceleration:= , Axis:=Axis , Done=> , CommandAborted=> , Error=> , ErrorID=> );
		IF MC_MoveRelative_1.Done THEN
			MC_MoveRelative_1(Execute:=FALSE , Distance:= , Velocity:= , Acceleration:= , Deceleration:= , Axis:=Axis , Done=> , CommandAborted=> , Error=> , ErrorID=> );
			diState	:=4;
		ELSIF MC_MoveRelative_1.Error OR (Axis.nAxisState = 1)  THEN
			T_WaitTime(IN:=FALSE , PT:=tiWaitTime , Q=> , ET=> );
			bError		:=TRUE;
			diState	:=100;
		ELSIF MC_MoveRelative_1.CommandAborted THEN
			T_WaitTime(IN:=FALSE , PT:=tiWaitTime , Q=> , ET=> );
			bCommandAborted	:=TRUE;
			diState	:=100;
		END_IF

	4:
		T_WaitTime(IN:=TRUE , PT:=tiWaitTime , Q=> , ET=> );
		IF NOT (bForward XOR bBackward) THEN
			bDone		:=TRUE;
			T_WaitTime(IN:=FALSE , PT:=tiWaitTime , Q=> , ET=> );
			diState	:=0;
		ELSIF T_WaitTime.Q THEN
			T_WaitTime(IN:=FALSE , PT:=tiWaitTime , Q=> , ET=> );
			diState	:=5;
		END_IF

	5:
		IF NOT (bForward XOR bBackward) THEN
			diState	:=0;
		ELSIF bForwardInternal AND NOT bBackwardInternal THEN
			MC_MoveVelocity_1.Direction	:=positive;
		ELSIF bBackwardInternal AND NOT bForwardInternal THEN
			MC_MoveVelocity_1.Direction	:=negative;
		END_IF
		IF bFast THEN
			MC_MoveVelocity_1.Velocity	:=rFastVelocity;
		ELSE
			MC_MoveVelocity_1.Velocity	:=rSlowVelocity;
		END_IF
		MC_MoveVelocity_1.Acceleration		:=rAcceleration;
		MC_MoveVelocity_1.Deceleration	:=rDeceleration;
		diState	:=6;

	6:
		MC_MoveVelocity_1(Execute:=TRUE , Velocity:= , Acceleration:= , Deceleration:= , Direction:= , Axis:=Axis , InVelocity=> , CommandAborted=> , Error=> , ErrorID=> );
		IF (bForward <> bForwardInternal) OR bBackward <> bBackwardInternal THEN
			MC_Stop_1(Execute:=TRUE ,Deceleration:=rDeceleration , Axis:=Axis, Done=> , Error=> , ErrorID=> );
			diState	:=7;
		ELSIF MC_MoveVelocity_1.CommandAborted THEN
			bCommandAborted		:=TRUE;
			diState	:=100;
		ELSIF MC_MoveVelocity_1.Error THEN
			bError		:=TRUE;
			diState	:=100;
		ELSE
			IF bFastInternal<>bFast THEN
				IF bFast THEN
					MC_MoveVelocity_1.Velocity	:=rFastVelocity;
				ELSE
					MC_MoveVelocity_1.Velocity	:=rSlowVelocity;
				END_IF
				MC_MoveVelocity_1(Execute:=FALSE , Velocity:= , Acceleration:= , Deceleration:= , Direction:= , Axis:=Axis , InVelocity=> , CommandAborted=> , Error=> , ErrorID=> );
				bFastInternal	:=bFast;
			END_IF
		END_IF
	7:
		MC_Stop_1(Execute:=TRUE ,Deceleration:=rDeceleration , Axis:=Axis, Done=> , Error=> , ErrorID=> );
		IF MC_Stop_1.Done THEN
			MC_Stop_1(Execute:=FALSE ,Deceleration:=rDeceleration , Axis:=Axis, Done=> , Error=> , ErrorID=> );
			MC_MoveVelocity_1(Execute:=FALSE , Velocity:= , Acceleration:= , Deceleration:= , Direction:= , Axis:=Axis , InVelocity=> , CommandAborted=> , Error=> , ErrorID=> );
			bDone		:=TRUE;
			diState	:=0;
		ELSIF MC_Stop_1.Error THEN
			MC_Stop_1(Execute:=FALSE ,Deceleration:=rDeceleration , Axis:=Axis, Done=> , Error=> , ErrorID=> );
			MC_MoveVelocity_1(Execute:=FALSE , Velocity:= , Acceleration:= , Deceleration:= , Direction:= , Axis:=Axis , InVelocity=> , CommandAborted=> , Error=> , ErrorID=> );
			bError		:=TRUE;
			diState	:=100;
		END_IF

	100:	(* Error *)
		bBusy	:=FALSE;
		MC_MoveRelative_1(Execute:=FALSE, Axis:=Axis);
		MC_MoveVelocity_1(Execute:=FALSE , Axis:=Axis);
		MC_Stop_1(Execute:=FALSE, Axis:=Axis);
		IF NOT bForward AND NOT bBackward THEN
			diState	:=0;
		END_IF
END_CASE
FUNCTION cmdReverse : TargetDirect
VAR_INPUT
	input		:TargetDirect;
END_VAR

IF input = TargetDirect.extend THEN
	cmdReverse := TargetDirect.retract;
END_IF
IF input = TargetDirect.retract THEN
	cmdReverse := TargetDirect.extend;
END_IF
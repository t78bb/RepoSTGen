FUNCTION_BLOCK Tank
VAR_INPUT
	stName: STRING;
	nMaxLevel	: INT;
	nMinLevel	: INT;
	nMaxTemp	: INT;
	nMinTemp	: INT;
	nUnitLevel							:INT:=0;
	nUnitTemp							:INT:=0;
END_VAR
VAR_OUTPUT
END_VAR
VAR
	name								:STRING;
	bLevel								:BOOL;
	bTemp								:BOOL;
END_VAR

name := stName;

IF(nUnitLevel > nMaxLevel) THEN
	bLevel := FALSE;
END_IF
IF(nUnitLevel < nMinLevel) THEN
	bLevel := TRUE;
END_IF

IF(bLevel) THEN
	nUnitLevel:=nUnitLevel+1;
ELSE
	nUnitLevel:=nUnitLevel-1;
END_IF

IF(nUnitTemp > nMaxTemp) THEN
	bTemp := FALSE;
END_IF
IF(nUnitTemp < nMinTemp) THEN
	bTemp := TRUE;
END_IF

IF(bTemp) THEN
	nUnitTemp:=nUnitTemp+1;
ELSE
	nUnitTemp:=nUnitTemp-1;
END_IF

METHOD PublishReceived : BOOL
VAR_INPUT
	(*Collection of received Data*)
	Data	: MQTT.CALLBACK_DATA;
	(*toggels lamp, sends publish*)	
	SwitchIn: BOOL;
END_VAR

VAR_OUTPUT
	LampOut: BOOL;

END_VAR
VAR
	MyInit: BOOL;
	SendState:MQTT.MQTTState;
	SwitchTrigger:R_TRIG;
END_VAR

//check if the packet is for me


IF CommonTypesAndFunctions.StrEquals(str1:= ADR(MyTopicReceive), str2:= Data.TopicOut) THEN
	PublishReceived := TRUE;//mark as done
	//now do the Commands
	IF CommonTypesAndFunctions.StrEquals(str1:= Data.PayloadString, str2:= ADR('Switch Lamp On')) THEN
		LampOut := TRUE;
	END_IF
	IF CommonTypesAndFunctions.StrEquals(str1:= Data.PayloadString, str2:= ADR('Switch Lamp Off')) THEN
		LampOut := FALSE;
	END_IF
END_IF 
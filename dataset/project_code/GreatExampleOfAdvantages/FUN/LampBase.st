FUNCTION_BLOCK LampBase EXTENDS TopicsBase IMPLEMENTS MQTT.MQTT_SUBSCRIBE_CALLBACK
VAR_INPUT
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

IF NOT MyInit THEN
	MyInit := TRUE;
	SUPER^();
	//this is for transmitting the lamp state
	(*SendState.Init(
	State:= ADR(LampOut), 
	Topic:= ADR(MyTopicSend), 
	StateName:= ADR(''), 
	StateValueOn:= ADR('Lamp switched On'), 
	StateValueOff:= ADR('Lamp switched Off'), 
	MQTT_IN_OUT REF= GVL_MQTT.MQTT_IN_OUT, 
	QoS:= SD_MQTT.QoS.ExactlyOnce,
	RetainMqtt:= TRUE);*)
	MyProperty.Collector.put(instance:= THIS^);
	SendState.Init(
	State:= ADR(LampOut), 
	Topic:= ADR(MyTopicSend), 
	StateName:= ADR(''), 
	MQTT_IN_OUT:= GVL_MQTT.MQTT_IN_OUT, 
	StateValueOn:= ADR('Lamp switched On'), 
	StateValueOff:= ADR('Lamp switched Off'), 
	QoS:= MQTT.QoS.ExactlyOnce, 
	RetainMqtt:= TRUE);
END_IF

SwitchTrigger(CLK:= SwitchIn);
IF SwitchTrigger.Q THEN
	LampOut := LampOut XOR 1;
END_IF
SendState();
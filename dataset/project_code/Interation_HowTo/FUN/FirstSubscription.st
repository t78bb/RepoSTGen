FUNCTION_BLOCK FirstSubscription
VAR_INPUT
END_VAR
VAR_OUTPUT
END_VAR
VAR
	collector:MQTT.CallbackCollector;
	SUB1:MQTT.MQTTSubscribe;
	init: BOOL;
	receiver:MQTT.ReceiveString;
END_VAR

IF NOT init THEN
	init := TRUE;
	SUB1.SetMqttInOut(MQTT_IN_OUT:= HowTo.MQTT_IN_OUT);
	collector.put(instance:= receiver);
	receiver.initAsFindTopic(compString:= ADR('TestTopic/FromCodesys'), returnHit:= TRUE);
END_IF

SUB1(
	Subscribe:= TRUE, 
	Topic:= ADR('TestTopic/FromCodesys'), 
	QoSSubscribe:= MQTT.QoS.ExactlyOnce, 
	ExpectingString:= TRUE, 
	Callback:= collector);
	
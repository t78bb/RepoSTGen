VAR
	publisher:MQTT.MQTTPublish;
	doPublish: BOOL;
	init: BOOL;
	sendPayload:STRING :='testPayload';
END_VAR

IF NOT init THEN
	init := TRUE;
	publisher.SetMqttInOut(MQTT_IN_OUT:= HowTo.MQTT_IN_OUT);
END_IF
publisher(
	Topic:= ADR('TestTopic/FromCodesys'), 
	PayloadString:= ADR(sendPayload), 
	PublishAsString:= TRUE, 
	QoSIn:= MQTT.QoS.ExactlyOnce, 
	MRetain:= FALSE, 
	send:= doPublish);
PROGRAM HowTo
VAR
	MQTT_IN_OUT:MQTT.MQTT_IN_OUT;
	//HandleMQTT:SD_MQTT.HANDLE_MQTT;
	FirstPublish:FirstPublish;
	FirstSubscription:FirstSubscription;
END_VAR

MQTT_IN_OUT.clientFB(
	MQTT_IN_OUT:= MQTT_IN_OUT, 
	ENABLE:= TRUE, 
	URL:= 'test.mosquitto.org:1883', 
	TIMEOUT:= T#2S, 
	TLS:= FALSE);
	
FirstPublish();
FirstSubscription();
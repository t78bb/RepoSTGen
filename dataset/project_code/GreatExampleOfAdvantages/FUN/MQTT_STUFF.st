FUNCTION_BLOCK MQTT_STUFF
VAR_INPUT
END_VAR
VAR_OUTPUT
END_VAR
VAR
	//Client:SD_MQTT.HANDLE_MQTT;
	
	Subscriber:MQTT.MQTTSubscribe;
	init: BOOL;
	InstanceName:CommonTypesAndFunctions.GetInstanceName;
	SubscribeTopic:STRING(255);
	birthTopic:STRING(255);
	found:DINT;
	pt:POINTER TO STRING;
	birthMessage:MQTT.MQTTPublish;
	connectRising:R_TRIG;
	xxx:POINTER TO STRING;
END_VAR

IF NOT init THEN
	init := TRUE;
	Subscriber.SetMqttInOut(MQTT_IN_OUT:= GVL_MQTT.MQTT_IN_OUT);
	SubscribeTopic := InstanceName.GetInstanceTopic();
	birthTopic := SubscribeTopic;
	found := CommonTypesAndFunctions.find(str1:= ADR(SubscribeTopic), str2:= ADR('/'));
	found := found + 1 + CommonTypesAndFunctions.find(str1:= ADR(SubscribeTopic[found + 1]), str2:= ADR('/'));
	pt := ADR(SubscribeTopic[found  + 1]);
	pt^ := 'Receive/#'; 
	GVL_MQTT.MQTT_IN_OUT.ClientID := CONCAT('CodesysMqtt',TO_STRING(TICKS.GetTick(xDummy:= TRUE)));
END_IF


GVL_MQTT.MQTT_IN_OUT.clientFB( 
	MQTT_IN_OUT:= GVL_MQTT.MQTT_IN_OUT, 
	ENABLE:= TRUE, 
	URL:= 'broker.hivemq.com:1883', 
	TIMEOUT:= T#8S);
	
Subscriber(
	Subscribe:= TRUE, 
	Topic:= ADR(SubscribeTopic), 
	QoSSubscribe:= MQTT.QoS.ExactlyOnce, 
	ExpectingString:= TRUE, 
	Callback:= MyProperty.Collector);
	
connectRising(CLK:= GVL_MQTT.MQTT_IN_OUT.BROKER_CONNECTED);

	birthMessage(
	Topic:= ADR(birthTopic), 
	PayloadString:= ADR('born'), 
	PublishAsString:= TRUE,
	QoSIn:= MQTT.QoS.ExactlyOnce , 
	MRetain:= FALSE, 
	send:= connectRising.Q);
	

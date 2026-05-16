(*this fb creats all topics an handles send and receive*)
FUNCTION_BLOCK TemperatureBase EXTENDS TopicsBase IMPLEMENTS MQTT.MQTT_SUBSCRIBE_CALLBACK
VAR_INPUT
	tempIn:REAL;
END_VAR
VAR_OUTPUT
END_VAR
	

VAR
	MyInit: BOOL;
	SendTemp:MQTT.MQTTValue;
	delimiter:BYTE;
	startValue:CommonTypesAndFunctions.ALL_TYPES_UNION;
	SetPoint:MQTT.ReceiveValue;
	SendPointer:CommonTypesAndFunctions.ALL_TYPES_UNION_POINTER;
	
END_VAR

IF NOT MyInit THEN
	MyInit := TRUE;
	SUPER^();
	SendPointer.POINTER_TO_REAL_T := ADR(tempIn);
	//prepare sending of acually temp
	SendTemp.Init(
	Topic:= ADR(MyTopicSend), 
	ValueName:= ADR(''), 
	ValuePointer:= SendPointer, 
	ValueType:= IBaseLibrary.TYPE_REAL, 
	ValueDiff:= 1, 
	MQTT_IN_OUT:= GVL_MQTT.MQTT_IN_OUT, 
	DecimalPlace:= 1, 
	QoS:= MQTT.QoS.ExactlyOnce, 
	RetainMqtt:= TRUE, 
	MinTime:= T#5S);
	//init receive of temp setpoint
	SetPoint.initAsFindTopicAndPayload(
	splitChar:= ':', 
	compStringTopic:= ADR(MyTopicReceive), 
	compStringpayload:= ADR('Set'), 
	ValueTyp:= CommonTypesAndFunctions.IBaseLibrary.TYPE_REAL, 
	returnHit:= TRUE);	
	
	MyProperty.Collector.put(THIS^);
	//init temp
	startValue.REAL_T := 22.0;
	SetPoint.SetOutput(value:= startValue); 
END_IF

//here yust call sending of temp
SendTemp();

//here make some logic for your temp....
//the setpoint can be found in SetPoint.MQTTreceived.REAL_T
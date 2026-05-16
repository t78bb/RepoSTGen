VAR
	MyInit: BOOL;
	SendTemp:MQTT.MQTTValue;
	delimiter:BYTE;
	startValue:CommonTypesAndFunctions.ALL_TYPES_UNION;
	SetPoint:MQTT.ReceiveValue;
	SendPointer:CommonTypesAndFunctions.ALL_TYPES_UNION_POINTER;
	
END_VAR


//check if the packet is for me


PublishReceived := SetPoint.PublishReceived(Data:= Data);
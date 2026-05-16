VAR
	//from this instance i can get my value...
	MQTTValue:MQTT.ReceiveValue;
	init: BOOL;
	{attribute 'instance-path'}
	{attribute 'noinit'}
	instanceName: STRING(255);//this string contains the instance name of the FB
	//here we get the "lowest" element of the name...
	LastTreeName:STRING;
	StringPointer:POINTER TO STRING;
END_VAR


PublishReceived := MQTTValue.PublishReceived(Data:= Data);

VAR
	InstanceName:CommonTypesAndFunctions.GetInstanceName;
	MyTopicSend:STRING(255);
	MyTopicReceive:STRING(255);
	init: BOOL;
END_VAR

IF NOT init THEN
	init := TRUE;
	//MyTopic := InstanceName.GetInstanceTopic();
	MyTopicSend := InsertSendToStringTopic(in:= InstanceName.GetInstanceTopic(), TopicLevel:= 1);
	MyTopicReceive := InsertReceiveToStringTopic(in:= InstanceName.GetInstanceTopic(), TopicLevel:= 1);
END_IF
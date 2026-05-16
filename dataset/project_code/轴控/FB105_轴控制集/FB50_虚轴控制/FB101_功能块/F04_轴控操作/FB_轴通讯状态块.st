FUNCTION_BLOCK FB_轴通讯状态块
VAR_INPUT
	Axis_bCommunication: BOOL;
	Axis_wCommunicationState: WORD;
END_VAR
VAR_OUTPUT
	EtherCATBusOK: BOOL;
END_VAR
VAR
END_VAR

EtherCATBusOK := (Axis_wCommunicationState = 100) AND Axis_bCommunication;

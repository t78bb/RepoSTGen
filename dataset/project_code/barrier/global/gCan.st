{attribute 'qualified_only'}
VAR_GLOBAL
	C6TxMsg			AT%QW00		:Can_BUS_8Outputs;	
	C6RxMsg			AT%IW00		:Can_BUS_8Inputs;
	C6RxCounter			 	   	:UINT;
	
	C3TxMsg			AT%QW52		:Can_BUS_8Outputs;	
	C3RxMsg			AT%IW47		:Can_BUS_8Inputs;
	C3RxCounter			   	   	:UINT;

	C4TxMsg			AT%QW104	:Can_BUS_8Outputs;	
	C4RxMsg			AT%IW94		:Can_BUS_8Inputs;
	C4RxCounter				  	:UINT;

	C2TxMsg			AT%QW156	:Can_BUS_8Outputs;	
	C2RxMsg			AT%IW141	:Can_BUS_8Inputs;
	C2RxCounter			 	   	:UINT;
//(*	
	C1TxMsg			AT%QW208	:Can_BUS_8Outputs;	
	C1RxMsg			AT%IW188	:Can_BUS_8Inputs;
	C1RxCounter			   	   	:UINT;

	C5TxMsg			AT%QW260	:Can_BUS_8Outputs;	
	C5RxMsg			AT%IW235	:Can_BUS_8Inputs;
	C5RxCounter				  	:UINT;
//*)

END_VAR
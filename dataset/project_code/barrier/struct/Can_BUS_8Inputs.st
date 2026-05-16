TYPE Can_BUS_8Inputs :          //输入缓存结构 EL2721-8Message_IN
STRUCT
	TxCounter			: UINT;
	RxCounter			: UINT;
	NoOfRxMessages 	 	: UINT;
	TransactionNumber	: UINT;
	RXMsg				: ARRAY[1..8] OF Can_Bus_RXMsg_Buff;
	CAN_State			: UINT;
	Align				: UINT;
	RX_Error_Cnt		: BYTE;
	TX_Error_Cnt		: BYTE;
END_STRUCT
END_TYPE

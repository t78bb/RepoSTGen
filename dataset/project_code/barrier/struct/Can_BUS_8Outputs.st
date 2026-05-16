TYPE Can_BUS_8Outputs :		//输出缓存结构 EL2721-8Message_OUT
STRUCT
	TxCounter		: UINT;
	RxCounter		: UINT;
	NoOfTxMessages 	: UINT;
	TXMsg			: ARRAY[1..8] OF Can_Bus_TXMsg_Buff;
	CAN_Control		: UINT;
END_STRUCT
END_TYPE

TYPE Can_Bus_TXMsg_Buff :
STRUCT
	TxMsg_TransactionNumber		: UINT;
	TxMsg_CobId					: UINT;
	TxMsg_Byte  				: ARRAY[1..8] OF BYTE;
END_STRUCT
END_TYPE

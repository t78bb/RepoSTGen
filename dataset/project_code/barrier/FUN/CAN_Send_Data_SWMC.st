FUNCTION CAN_Send_Data_SWMC : BOOL
VAR_INPUT
	SWMC_ID : UINT;
	id 		: UINT;
	data	: ARRAY[1..8] OF BYTE;
END_VAR
VAR
	
END_VAR

CASE  SWMC_ID OF

	1:
		gCan.C1TxMsg.TXMsg[1].TxMsg_CobId 	:= 8 + 32 * id;
	  	gCan.C1TxMsg.TXMsg[1].TxMsg_Byte 	:= data;
	   	gCan.C1TxMsg.NoOfTxMessages			:= 1;
	   	gCan.C1TxMsg.TxCounter 				:= gCan.C1TxMsg.TxCounter +1;	
	2:
		gCan.C2TxMsg.TXMsg[1].TxMsg_CobId 	:= 8 + 32 * id;
	  	gCan.C2TxMsg.TXMsg[1].TxMsg_Byte 	:= data;
	   	gCan.C2TxMsg.NoOfTxMessages			:= 1;
	   	gCan.C2TxMsg.TxCounter 				:= gCan.C2TxMsg.TxCounter +1;	
	3:
		gCan.C3TxMsg.TXMsg[1].TxMsg_CobId 	:= 8 + 32 * id;
	  	gCan.C3TxMsg.TXMsg[1].TxMsg_Byte 	:= data;
	   	gCan.C3TxMsg.NoOfTxMessages			:= 1;
	   	gCan.C3TxMsg.TxCounter 				:= gCan.C3TxMsg.TxCounter +1;
	4:
		gCan.C4TxMsg.TXMsg[1].TxMsg_CobId 	:= 8 + 32 * id;
	  	gCan.C4TxMsg.TXMsg[1].TxMsg_Byte 	:= data;
	   	gCan.C4TxMsg.NoOfTxMessages			:= 1;
	   	gCan.C4TxMsg.TxCounter 				:= gCan.C4TxMsg.TxCounter +1;
	//(*
	5:
		gCan.C5TxMsg.TXMsg[1].TxMsg_CobId 	:= 8 + 32 * id;
	  	gCan.C5TxMsg.TXMsg[1].TxMsg_Byte 	:= data;
	   	gCan.C5TxMsg.NoOfTxMessages			:= 1;
	   	gCan.C5TxMsg.TxCounter 				:= gCan.C5TxMsg.TxCounter +1;
	6:
		gCan.C6TxMsg.TXMsg[1].TxMsg_CobId 	:= 8 + 32 * id;
	  	gCan.C6TxMsg.TXMsg[1].TxMsg_Byte 	:= data;
	   	gCan.C6TxMsg.NoOfTxMessages			:= 1;
	   	gCan.C6TxMsg.TxCounter 				:= gCan.C6TxMsg.TxCounter +1;
	//*)

END_CASE
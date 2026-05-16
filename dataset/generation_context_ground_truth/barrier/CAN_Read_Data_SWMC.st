VAR
	frame :Can_baseframe;
END_VAR

CASE  SWMC_ID OF

	1:                       //SWMC-C1
		frame.id 	:= (gCan.C1RxMsg.RXMsg[I].RxMsg_CobId-8)/32;
		frame.data 	:= gCan.C1RxMsg.RXMsg[I].RxMsg_Byte;				
	2:                       //SWMC-C2
		frame.id 	:= (gCan.C2RxMsg.RXMsg[I].RxMsg_CobId-8)/32;
		frame.data 	:= gCan.C2RxMsg.RXMsg[I].RxMsg_Byte;
	3:						//SWMC-C3
		frame.id 	:= (gCan.C3RxMsg.RXMsg[I].RxMsg_CobId-8)/32;
		frame.data 	:= gCan.C3RxMsg.RXMsg[I].RxMsg_Byte;	
	4:                       //SWMC-C4
		frame.id 	:= (gCan.C4RxMsg.RXMsg[I].RxMsg_CobId-8)/32;
		frame.data 	:= gCan.C4RxMsg.RXMsg[I].RxMsg_Byte;				
	//(*
	5:                       //SWMC-C5
		frame.id 	:= (gCan.C5RxMsg.RXMsg[I].RxMsg_CobId-8)/32;
		frame.data 	:= gCan.C5RxMsg.RXMsg[I].RxMsg_Byte;
	6:						//SWMC-C6
		frame.id 	:= (gCan.C6RxMsg.RXMsg[I].RxMsg_CobId-8)/32;
		frame.data 	:= gCan.C6RxMsg.RXMsg[I].RxMsg_Byte;	
		//*)
	ELSE				//Other
		frame.id := 0;
		frame.data[1] := 0;
		frame.data[2] := 0;
		frame.data[3] := 0;
		frame.data[4] := 0;
		frame.data[5] := 0;
		frame.data[6] := 0;
		frame.data[7] := 0;
		frame.data[8] := 0;
END_CASE
Can_Read_data_SWMC := frame;
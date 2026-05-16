METHOD C02_Tx
VAR_INPUT
END_VAR
VAR
	swmcIdSwtich		:UINT;
	sendData			:ARRAY[1..8] OF BYTE;
END_VAR


swmcIdSwtich := count MOD 2;
CASE swmcIdSwtich OF
	0:
		sendData[1] := WORD_TO_BYTE(gController.sky[0].extendPercent);
		sendData[2] := WORD_TO_BYTE(SHR(gController.sky[0].extendPercent,8));
		sendData[3] := WORD_TO_BYTE(gController.sky[0].retractPercent);
		sendData[4] := WORD_TO_BYTE(SHR(gController.sky[0].retractPercent,8));
		sendData[5] := WORD_TO_BYTE(gController.sky[1].extendPercent);
		sendData[6] := WORD_TO_BYTE(SHR(gController.sky[1].extendPercent,8));
		sendData[7] := WORD_TO_BYTE(gController.sky[1].retractPercent);
		sendData[8] := WORD_TO_BYTE(SHR(gController.sky[1].retractPercent,8));
		CAN_Send_Data_SWMC(2, 16#510,senddata);   //发送ID 0x460到C6
		
	1:
		sendData[1] := WORD_TO_BYTE(gController.sky[2].extendPercent);
		sendData[2] := WORD_TO_BYTE(SHR(gController.sky[2].extendPercent,8));
		sendData[3] := WORD_TO_BYTE(gController.sky[2].retractPercent);
		sendData[4] := WORD_TO_BYTE(SHR(gController.sky[2].retractPercent,8));
		CAN_Send_Data_SWMC(2, 16#511,senddata);   //发送ID 0x460到C6
		
		


END_CASE
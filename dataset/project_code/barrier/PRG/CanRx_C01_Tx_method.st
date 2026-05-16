METHOD C01_Tx
VAR_INPUT
END_VAR
VAR
	swmcIdSwtich		:UINT;
	sendData			:ARRAY[1..8] OF BYTE;
END_VAR


swmcIdSwtich := count MOD 2;
CASE swmcIdSwtich OF
	0:
		sendData[1] := WORD_TO_BYTE(gController.sky[3].extendPercent);
		sendData[2] := WORD_TO_BYTE(SHR(gController.sky[3].extendPercent,8));
		sendData[3] := WORD_TO_BYTE(gController.sky[3].retractPercent);
		sendData[4] := WORD_TO_BYTE(SHR(gController.sky[3].retractPercent,8));
		sendData[5] := WORD_TO_BYTE(gController.sky[4].extendPercent);
		sendData[6] := WORD_TO_BYTE(SHR(gController.sky[4].extendPercent,8));
		sendData[7] := WORD_TO_BYTE(gController.sky[4].retractPercent);
		sendData[8] := WORD_TO_BYTE(SHR(gController.sky[4].retractPercent,8));
		CAN_Send_Data_SWMC(1, 16#500,senddata);   //发送ID 0x460到C6
		
	1:
		sendData[1] := WORD_TO_BYTE(gController.sky[5].extendPercent);
		sendData[2] := WORD_TO_BYTE(SHR(gController.sky[5].extendPercent,8));
		sendData[3] := WORD_TO_BYTE(gController.sky[5].retractPercent);
		sendData[4] := WORD_TO_BYTE(SHR(gController.sky[5].retractPercent,8));
		sendData[5] := WORD_TO_BYTE(gController.sky[6].extendPercent);
		sendData[6] := WORD_TO_BYTE(SHR(gController.sky[6].extendPercent,8));
		sendData[7] := WORD_TO_BYTE(gController.sky[6].retractPercent);
		sendData[8] := WORD_TO_BYTE(SHR(gController.sky[6].retractPercent,8));
		CAN_Send_Data_SWMC(1, 16#501,senddata);   //发送ID 0x460到C6
		
		


END_CASE
METHOD C06_Tx
VAR_INPUT
END_VAR
VAR
	swmcIdSwtich		:UINT;
	sendData			:ARRAY[1..8] OF BYTE;
END_VAR


swmcIdSwtich := count MOD 2;
CASE swmcIdSwtich OF
	0:
		sendData[1] := WORD_TO_BYTE(gController.grd[7].extendPercent);
		sendData[2] := WORD_TO_BYTE(SHR(gController.grd[7].extendPercent,8));
		sendData[3] := WORD_TO_BYTE(gController.grd[7].retractPercent);
		sendData[4] := WORD_TO_BYTE(SHR(gController.grd[7].retractPercent,8));
		sendData[5] := WORD_TO_BYTE(gController.grd[8].extendPercent);
		sendData[6] := WORD_TO_BYTE(SHR(gController.grd[8].extendPercent,8));
		sendData[7] := WORD_TO_BYTE(gController.grd[8].retractPercent);
		sendData[8] := WORD_TO_BYTE(SHR(gController.grd[8].retractPercent,8));
		CAN_Send_Data_SWMC(6, 16#550,senddata);   //发送ID 0x460到C6
		
	1:
		sendData[1] := WORD_TO_BYTE(gController.grd[9].extendPercent);
		sendData[2] := WORD_TO_BYTE(SHR(gController.grd[9].extendPercent,8));
		sendData[3] := WORD_TO_BYTE(gController.grd[9].retractPercent);
		sendData[4] := WORD_TO_BYTE(SHR(gController.grd[9].retractPercent,8));
		sendData[5] := WORD_TO_BYTE(gController.grd[10].extendPercent);
		sendData[6] := WORD_TO_BYTE(SHR(gController.grd[10].extendPercent,8));
		sendData[7] := WORD_TO_BYTE(gController.grd[10].retractPercent);
		sendData[8] := WORD_TO_BYTE(SHR(gController.grd[10].retractPercent,8));
		CAN_Send_Data_SWMC(6, 16#551,senddata);   //发送ID 0x460到C6
		
END_CASE
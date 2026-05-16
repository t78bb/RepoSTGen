METHOD C02_Rx
VAR_INPUT
END_VAR
VAR
	frame	 	    :Can_baseframe;
	I				:UINT;
	fId				:UINT;
	pos				:WORD;
	spd				:WORD;
END_VAR

IF gCan.C2RxMsg.RxCounter <>  gCan.C2RxCounter THEN    //接收到新的数据
	FOR I := 1 TO gCan.C2RxMsg.NoOfRxMessages DO
		frame := CAN_Read_Data_SWMC(2,I);
		fId := frame.id;
		CASE fId OF
			16#610:
				pos := BYTE_TO_WORD(frame.data[ 1 ]) OR SHL(BYTE_TO_WORD(frame.data[ 2 ]),8);
				gDev.sky[0].sensor.position := pos * 0.1;
				pos := BYTE_TO_WORD(frame.data[ 3 ]) OR SHL(BYTE_TO_WORD(frame.data[ 4 ]),8);
				gDev.sky[1].sensor.position := pos * 0.1;
				pos := BYTE_TO_WORD(frame.data[ 5 ]) OR SHL(BYTE_TO_WORD(frame.data[ 6 ]),8);
				gDev.sky[2].sensor.position := pos * 0.1;
	
			16#611:
				spd := BYTE_TO_WORD(frame.data[ 1 ]) OR SHL(BYTE_TO_WORD(frame.data[ 2 ]),8);
				gDev.sky[0].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
				spd := BYTE_TO_WORD(frame.data[ 3 ]) OR SHL(BYTE_TO_WORD(frame.data[ 4 ]),8);
				gDev.sky[1].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
				spd := BYTE_TO_WORD(frame.data[ 5 ]) OR SHL(BYTE_TO_WORD(frame.data[ 6 ]),8);
				gDev.sky[2].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
		END_CASE
	END_FOR
	gCan.C2RxCounter := gCan.C2RxMsg.RxCounter;
END_IF
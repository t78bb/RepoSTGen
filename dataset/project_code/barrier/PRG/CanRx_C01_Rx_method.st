METHOD C01_Rx
VAR_INPUT
END_VAR
VAR
	frame	 	    :Can_baseframe;
	I				:UINT;
	fId				:UINT;
	pos				:WORD;
	spd				:WORD;
END_VAR

IF gCan.C1RxMsg.RxCounter <>  gCan.C1RxCounter THEN    //接收到新的数据
	FOR I := 1 TO gCan.C1RxMsg.NoOfRxMessages DO
		frame := CAN_Read_Data_SWMC(1,I);
		fId := frame.id;
		CASE fId OF
			16#600:
				pos := BYTE_TO_WORD(frame.data[ 1 ]) OR SHL(BYTE_TO_WORD(frame.data[ 2 ]),8);
				gDev.sky[4].sensor.position := pos * 0.1;
				pos := BYTE_TO_WORD(frame.data[ 3 ]) OR SHL(BYTE_TO_WORD(frame.data[ 4 ]),8);
				gDev.sky[5].sensor.position := pos * 0.1;
				pos := BYTE_TO_WORD(frame.data[ 5 ]) OR SHL(BYTE_TO_WORD(frame.data[ 6 ]),8);
				gDev.sky[6].sensor.position := pos * 0.1;
				pos := BYTE_TO_WORD(frame.data[ 7 ]) OR SHL(BYTE_TO_WORD(frame.data[ 8 ]),8);
				gDev.sky[3].sensor.position := pos * 0.1;
			16#601:
				spd := BYTE_TO_WORD(frame.data[ 1 ]) OR SHL(BYTE_TO_WORD(frame.data[ 2 ]),8);
				gDev.sky[4].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
				spd := BYTE_TO_WORD(frame.data[ 3 ]) OR SHL(BYTE_TO_WORD(frame.data[ 4 ]),8);
				gDev.sky[5].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
				spd := BYTE_TO_WORD(frame.data[ 5 ]) OR SHL(BYTE_TO_WORD(frame.data[ 6 ]),8);
				gDev.sky[6].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
				spd := BYTE_TO_WORD(frame.data[ 7 ]) OR SHL(BYTE_TO_WORD(frame.data[ 8 ]),8);
				gDev.sky[3].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
		END_CASE

	END_FOR
	gCan.C1RxCounter := gCan.C1RxMsg.RxCounter;
END_IF
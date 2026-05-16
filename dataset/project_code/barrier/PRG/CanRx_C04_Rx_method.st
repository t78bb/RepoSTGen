METHOD C04_Rx
VAR_INPUT
END_VAR
VAR
	frame	 	    :Can_baseframe;
	I				:UINT;
	fId				:UINT;
	pos				:WORD;
	spd				:WORD;
	
END_VAR

IF gCan.C4RxMsg.RxCounter <>  gCan.C4RxCounter THEN    //接收到新的数据
	FOR I := 1 TO gCan.C4RxMsg.NoOfRxMessages DO
		frame := CAN_Read_Data_SWMC(4,I);
		fId := frame.id;
		CASE fId OF
			16#630:
				pos := BYTE_TO_WORD(frame.data[ 1 ]) OR SHL(BYTE_TO_WORD(frame.data[ 2 ]),8);
				gDev.grd[1].sensor.position := pos * 0.1;
				pos := BYTE_TO_WORD(frame.data[ 3 ]) OR SHL(BYTE_TO_WORD(frame.data[ 4 ]),8);
				gDev.grd[2].sensor.position := pos * 0.1;
	
			16#631:
				spd := BYTE_TO_WORD(frame.data[ 1 ]) OR SHL(BYTE_TO_WORD(frame.data[ 2 ]),8);
				gDev.grd[1].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
				spd := BYTE_TO_WORD(frame.data[ 3 ]) OR SHL(BYTE_TO_WORD(frame.data[ 4 ]),8);
				gDev.grd[2].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
		END_CASE
	END_FOR
	gCan.C4RxCounter := gCan.C4RxMsg.RxCounter;
END_IF

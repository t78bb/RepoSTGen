METHOD C06_Rx
VAR_INPUT
END_VAR
VAR
	frame	 	    :Can_baseframe;
	I				:UINT;
	fId				:UINT;
	pos				:WORD;	//位置
	spd				:WORD;	//速度
END_VAR

IF gCan.C6RxMsg.RxCounter <>  gCan.C6RxCounter THEN    //接收到新的数据
	FOR I := 1 TO gCan.C6RxMsg.NoOfRxMessages DO
		frame := CAN_Read_Data_SWMC(6,I);
		fId := frame.id;
		CASE fId OF
			16#650:
				pos := BYTE_TO_WORD(frame.data[ 1 ]) OR SHL(BYTE_TO_WORD(frame.data[ 2 ]),8);
				gDev.grd[7].sensor.position := pos * 0.1;
				pos := BYTE_TO_WORD(frame.data[ 3 ]) OR SHL(BYTE_TO_WORD(frame.data[ 4 ]),8);
				gDev.grd[8].sensor.position := pos * 0.1;
				pos := BYTE_TO_WORD(frame.data[ 5 ]) OR SHL(BYTE_TO_WORD(frame.data[ 6 ]),8);
				gDev.grd[9].sensor.position := pos * 0.1;
				pos := BYTE_TO_WORD(frame.data[ 7 ]) OR SHL(BYTE_TO_WORD(frame.data[ 8 ]),8);
				gDev.grd[10].sensor.position := pos * 0.1;
			16#651:
				spd := BYTE_TO_WORD(frame.data[ 1 ]) OR SHL(BYTE_TO_WORD(frame.data[ 2 ]),8);
				gDev.grd[7].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
				spd := BYTE_TO_WORD(frame.data[ 3 ]) OR SHL(BYTE_TO_WORD(frame.data[ 4 ]),8);
				gDev.grd[8].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
				spd := BYTE_TO_WORD(frame.data[ 5 ]) OR SHL(BYTE_TO_WORD(frame.data[ 6 ]),8);
				gDev.grd[9].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
				spd := BYTE_TO_WORD(frame.data[ 7 ]) OR SHL(BYTE_TO_WORD(frame.data[ 8 ]),8);
				gDev.grd[10].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));	
		END_CASE
	END_FOR
	gCan.C6RxCounter := gCan.C6RxMsg.RxCounter;
END_IF
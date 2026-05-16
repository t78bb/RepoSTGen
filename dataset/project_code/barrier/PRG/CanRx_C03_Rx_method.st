METHOD C03_Rx
VAR_INPUT
END_VAR
VAR
	frame	 	    :Can_baseframe;
	I				:UINT;
	fId				:UINT;
	pos				:WORD;
	spd				:WORD;
	cur				:WORD;	//current
END_VAR

IF gCan.C3RxMsg.RxCounter <>  gCan.C3RxCounter THEN    //接收到新的数据
	FOR I := 1 TO gCan.C3RxMsg.NoOfRxMessages DO
		frame := CAN_Read_Data_SWMC(3,I);
		fId := frame.id;
		CASE fId OF
			16#620:
				pos := BYTE_TO_WORD(frame.data[ 1 ]) OR SHL(BYTE_TO_WORD(frame.data[ 2 ]),8);
				gDev.grd[5].sensor.position := pos * 0.1;
				pos := BYTE_TO_WORD(frame.data[ 3 ]) OR SHL(BYTE_TO_WORD(frame.data[ 4 ]),8);
				gDev.grd[6].sensor.position := pos * 0.1;
				pos := BYTE_TO_WORD(frame.data[ 5 ]) OR SHL(BYTE_TO_WORD(frame.data[ 6 ]),8);
				gDev.grd[3].sensor.position := pos * 0.1;
				pos := BYTE_TO_WORD(frame.data[ 7 ]) OR SHL(BYTE_TO_WORD(frame.data[ 8 ]),8);
				gDev.grd[4].sensor.position := pos * 0.1;
			16#621:
				spd := BYTE_TO_WORD(frame.data[ 1 ]) OR SHL(BYTE_TO_WORD(frame.data[ 2 ]),8);
				gDev.grd[5].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
				spd := BYTE_TO_WORD(frame.data[ 3 ]) OR SHL(BYTE_TO_WORD(frame.data[ 4 ]),8);
				gDev.grd[6].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
				spd := BYTE_TO_WORD(frame.data[ 5 ]) OR SHL(BYTE_TO_WORD(frame.data[ 6 ]),8);
				gDev.grd[3].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));
				spd := BYTE_TO_WORD(frame.data[ 7 ]) OR SHL(BYTE_TO_WORD(frame.data[ 8 ]),8);
				gDev.grd[4].sensor.speed := INT_TO_REAL(WORD_TO_INT(spd));	
			16#622:
				cur := BYTE_TO_WORD(frame.data[ 1 ]) OR SHL(BYTE_TO_WORD(frame.data[ 2 ]),8);
				gDev.grd[3].current[1] := cur;
				cur := BYTE_TO_WORD(frame.data[ 3 ]) OR SHL(BYTE_TO_WORD(frame.data[ 4 ]),8);
				gDev.grd[3].current[2] := cur;
				cur := BYTE_TO_WORD(frame.data[ 5 ]) OR SHL(BYTE_TO_WORD(frame.data[ 6 ]),8);
				gDev.grd[4].current[1] := cur;
				cur := BYTE_TO_WORD(frame.data[ 7 ]) OR SHL(BYTE_TO_WORD(frame.data[ 8 ]),8);
				gDev.grd[4].current[2] := cur;
			16#623:
				cur := BYTE_TO_WORD(frame.data[ 1 ]) OR SHL(BYTE_TO_WORD(frame.data[ 2 ]),8);
				gDev.grd[5].current[1] := cur;
				cur := BYTE_TO_WORD(frame.data[ 3 ]) OR SHL(BYTE_TO_WORD(frame.data[ 4 ]),8);
				gDev.grd[5].current[2] := cur;
				cur := BYTE_TO_WORD(frame.data[ 5 ]) OR SHL(BYTE_TO_WORD(frame.data[ 6 ]),8);
				gDev.grd[6].current[1] := cur;
				cur := BYTE_TO_WORD(frame.data[ 7 ]) OR SHL(BYTE_TO_WORD(frame.data[ 8 ]),8);
				gDev.grd[6].current[2] := cur;
				
				
				
		END_CASE
	END_FOR
	gCan.C3RxCounter := gCan.C3RxMsg.RxCounter;
END_IF
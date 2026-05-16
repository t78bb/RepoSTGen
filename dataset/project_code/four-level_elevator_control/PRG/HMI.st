PROGRAM HMI
VAR
	fbTon3s	:	Standard.TON;  //从电梯离开当前层起，定时3S，到达下一层
	fbTonOpen	:	Standard.TON; //电梯门1s开到位
	fbTonClose	:	Standard.TON;//电梯门1s关到位
	fbTon500ms	:	Standard.TON;//电梯关门后500ms电梯运动
	fbIsFloorFtrig		:	ARRAY[1..MaxNumFloor] OF Standard.F_TRIG;
	i	:	USINT;
	bTiming	:	BOOL;
	bTimingOpen	:	BOOL;
	bTimingClose	:	BOOL;
	isInWhichFloor	:	USINT;//电梯现在处在哪一层
	
	bhideLiftUp	:	BOOL;// 隐藏上升箭头
	bHideLiftDown	:	BOOL;  // 隐藏下降箭头
	bHideOpen	:	BOOL;  // 隐藏电梯门开箭头
	bHideClose	:	BOOL; // 隐藏电梯门关箭头
	
	fbMotorNegativeRunRtrig	:	Standard.R_TRIG;//电梯状态变成下降时触发的上升沿
	fbMotorPositiveRunRtrig	:	Standard.R_TRIG;//电梯状态变成上升时触发的上升沿
	
	fbOpenRtrig	:	Standard.R_TRIG;  //电梯门状态变成开时触发的上升沿
	fbCloseRtrig	:	Standard.R_TRIG;//电梯门状态变成关时触发的上升沿
	
	fbIsFloorRtrig	:	ARRAY[1..MaxNumFloor] OF Standard.R_TRIG;//电梯到达某层时触发当前层的上升沿
	bIsStop	:	BOOL;
	bNotStop	:	BOOL;
END_VAR

//判断什么时候显示电梯向上或者向下运动
bhideLiftUp := QMotorNegativeRun OR (NOT QMotorNegativeRun AND NOT QMotorPositiveRun);///向下运动或停止时隐藏上升箭头
bhideLiftDown := QMotorPositiveRun OR (NOT QMotorNegativeRun AND NOT QMotorPositiveRun);///向上运动或停止隐藏下降箭头

//判断什么时候复位IIsFloor[i]                      ///判断若在某层停下，则isstop 否则notStop
FOR i := 1 TO MaxNumFloor DO
	fbIsFloorRtrig[i](CLK := IIsFloor[i]);   //如电梯到达i层
	IF fbIsFloorRtrig[i].Q THEN
		IF (NOT QMotorNegativeRun) AND (NOT QMotorPositiveRun) THEN  //若电梯没有向上运动也没有向下运动，则电梯在i层停下，bIsStop为TRUE
			bIsStop := TRUE;
			EXIT;
		END_IF
		IF NOT bIsStop THEN
			bNotStop := TRUE;
		END_IF
	END_IF
END_FOR

fbTon500ms(IN := bNotStop,PT := T#500MS);            //电梯关门后500ms电梯运动
IF fbTon500ms.Q THEN
	IIsFloor[Tar_Dir.IsInWhichFloor] := FALSE;        
	bNotStop := FALSE;                               
END_IF

IF bIsStop THEN                      ///停止状态时若有向上或向下运动请求时,则该层的“电梯到位”置为FALSE,IsStop为FALSE
	fbMotorNegativeRunRtrig(CLK := QMotorNegativeRun);
	fbMotorPositiveRunRtrig(CLK := QMotorPositiveRun);
	IF fbMotorNegativeRunRtrig.Q OR fbMotorPositiveRunRtrig.Q THEN
		IIsFloor[Tar_Dir.IsInWhichFloor] := FALSE;
		bIsStop := FALSE;                          
	END_IF
END_IF


//从电梯离开当前层起，定时3S，到达下一层
//判断什么时候置位IIsFloor[i]
FOR i := 1 TO MaxNumFloor DO
	fbIsFloorFtrig[i](CLK := IIsFloor[i]);
	IF fbIsFloorFtrig[i].Q THEN
		bTiming := TRUE;
		isInWhichFloor := i;
		EXIT;
	END_IF
END_FOR

fbTon3s(IN := bTiming,PT := T#3S);
IF fbTon3s.Q THEN
	bTiming := FALSE;
	IF QMotorPositiveRun THEN
		IIsFloor[isInWhichFloor + 1] := TRUE;
	END_IF
	IF QMotorNegativeRun THEN
		IIsFloor[isInWhichFloor - 1] := TRUE;
	END_IF
END_IF

//电梯门1s开、关到位
fbOpenRtrig(CLK := QOpen);
fbCloseRtrig(CLK := QClose);
IF fbOpenRtrig.Q THEN
	bTimingOpen := TRUE;
	bTimingClose := FALSE;
	IIsClose := FALSE;
END_IF
IF fbCloseRtrig.Q THEN
	bTimingClose := TRUE;
	bTimingOpen := FALSE;
	IIsOpen := FALSE;
END_IF

fbTonOpen(IN := bTimingOpen,PT := T#1S);
IF fbTonOpen.Q THEN
	bTimingOpen := FALSE;
	IIsOpen :=TRUE;
END_IF

fbTonClose(IN := bTimingClose,PT := T#1S);
IF fbTonClose.Q THEN
	bTimingClose := FALSE;
	IIsClose :=TRUE;
END_IF

bHideOpen := bTimingClose OR (NOT bTimingClose AND NOT bTimingOpen);         //隐藏电梯开门箭头
bHideClose := bTimingOpen OR (NOT bTimingClose AND NOT bTimingOpen);           //隐藏电梯关门箭头
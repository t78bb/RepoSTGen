VAR
	fCycle			:REAL;    
	CycleTime		:TIME ;
	Err				:REAL;    		//本次误差
	LastErr			:REAL;    		//上次误差
	KiErrSum		:REAL;			//积分累计误差
	KdErr			:REAL;			//微分误差
	Result			:REAL;			//计算结果
	Result_OUT		:REAL;		    //限制结果
	trig			:R_TRIG ;
	ton				:TON ;
END_VAR

IF  rCycle < 0.01 THEN  //10ms最小
	fCycle := 0.01;
ELSE
	fCycle := rCycle;
END_IF

CycleTime := REAL_TO_TIME (TIME_TO_REAL(T#1S) * fCycle);
ton (IN := NOT ton.Q ,PT := CycleTime ,Q =>);
trig (CLK := ton.Q  ,Q =>);

IF trig.Q THEN 			//PID计算
	Err := Set_Val - Act_Val;  //误差计算
	KiErrSum := KiErrSum + Err ;   //积分计算
	KdErr := Err -LastErr;    //微分计算
	LastErr := Err;
	(*IF ABS(Err) < 10 THEN		//误差较低时才开启积分
		KiErrSum := KiErrSum + Err ;   //积分计算
	END_IF*)
	Result :=  Kp * Err + Ki * KiErrSum + Kd * KdErr;  
END_IF

IF Result > Y_MAX  THEN         //限幅度输出
	Result_OUT := Y_MAX ;
	LimitActive := TRUE ;
ELSIF Result < Y_MIN THEN
	Result_OUT := Y_MIN  ;
	LimitActive := TRUE ;
ELSE 
	Result_OUT := Result ;
	LimitActive :=FALSE ;
END_IF
IF Reset THEN   //pid 不输出
	KiErrSum := 0;
	KdErr := 0;
	LastErr	:= 0;
	Y := 0;
ELSE
	Y := Result_OUT;	
END_IF
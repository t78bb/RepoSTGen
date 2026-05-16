VAR
	posPid		:BasePIDCtrl;
	spdPid		:BasePIDCtrl;
	setSpeed	:REAL;
	overBase	:REAL;
	out			:REAL;
	//fb_Val		:REAL;
	controller	:DevPid;
END_VAR

controller := gDev.sky[idx].ctrl;
posPid(
	Act_Val:= gDev.sky[idx].sensor.position, 
	Set_Val:= controller.pos.Set_Point,
	Kp:= controller.pos.Kp, 
	Ki:= controller.pos.Ki, 
	Kd:= controller.pos.Kd, 
	Y_MAX:= controller.pos.Max_Val,     //最大速度
	Y_MIN:= -controller.pos.Max_Val,    //水平运动正反一致
	rCycle:= 0.05,   //位置计算周期 100ms
	Reset:= isReset, 
	Y => controller.pos.OUT, 
	LimitActive=> );

IF ABS(posPid.Y - setSpeed) > (cycTimer * controller.pos.Max_ACC) THEN
	IF posPid.Y > setSpeed THEN
		setSpeed := setSpeed + (cycTimer * controller.pos.Max_ACC);
	ELSE
		setSpeed := setSpeed - (cycTimer * controller.pos.Max_ACC);
	END_IF
ELSE
	setSpeed := posPid.Y;
END_IF

controller.spd.Set_Point := setSpeed;

IF setSpeed > 0 THEN
	overBase := setSpeed * controller.ff.pstKv + controller.ff.pstThreshold;
END_IF
IF setSpeed < 0 THEN	
	overBase := setSpeed * controller.ff.negKv - controller.ff.negThreshold;
END_IF

spdPid(
	Act_Val:= gDev.sky[idx].sensor.speed, 
	Set_Val:= controller.spd.Set_Point,
	Kp:= controller.spd.Kp, 
	Ki:= controller.spd.Ki, 
	Kd:= controller.spd.Kd, 
	Y_MAX:= controller.spd.Max_Val,     //最大速度
	Y_MIN:= -controller.spd.Max_Val,    //水平运动正反一致
	rCycle:= 0.02,   //位置计算周期 100ms
	Reset:= isReset, 
	Y=> , 
	LimitActive=> );

out := spdPid.Y + overBase;	

	
IF out > controller.spd.Max_Val THEN
	out := controller.spd.Max_Val;
END_IF
IF out < -controller.spd.Max_Val THEN
	out := -controller.spd.Max_Val;
END_IF
IF isReset	THEN out := 0;	END_IF
controller.spd.OUT := out;
gDev.sky[idx].ctrl := controller;
res := out;
PROGRAM Test_PID_Heatx
VAR
	PID_0: PID_controller;
	Process_out: REAL := 100;
	SetPoint: REAL := 20;
	A_room_with_a_view: HeatExchanger;
END_VAR

VAR CONSTANT
END_VAR

PID_0(
    SP := SetPoint,
    PV := A_room_with_a_view.PV,
    Kc := 5.0,
    Ti := 10.0,
    Td := 1.0,
    SampleTime := T#2000ms,
    LowerLimit := 0,
    UpperLimit := 150,
    CO => ,  // 若不需要单独使用 CO 等输出，可留空，或根据需求定义变量接收
    CO_P => ,
    CO_I => ,
    CO_D => 
);

// 调用 HeatExchanger 功能块
A_room_with_a_view(
    Kp := 2.0,
    Tp := 20,
    CO := PID_0.CO,
    Dead_t := 9.8,
    C := 2.048,
    Sample_time := T#100ms,
    PV => 
);
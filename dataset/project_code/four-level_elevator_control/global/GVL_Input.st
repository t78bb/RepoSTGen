VAR_GLOBAL
	IGoFloor	:	ARRAY[1..MaxNumFloor] OF BOOL;  //电梯里面
	ICallHelp	:	BOOL;
	IClose		:	BOOL;
	IOpen		:	BOOL;
	IIsClose	:	BOOL;
	IIsOpen		:	BOOL;
	
	IIsFloor	:	ARRAY[1..MaxNumFloor] OF BOOL := [TRUE];//电梯停在一层
	
	IFloorUp	:	ARRAY[1..MaxNumFloor - 1] OF BOOL; //电梯外面
	IFloorDown	:	ARRAY[2..MaxNumFloor] OF BOOL;

	IReset		:	BOOL;
	IRespondHelp	:	BOOL;
END_VAR
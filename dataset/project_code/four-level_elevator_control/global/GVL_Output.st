VAR_GLOBAL
	QMotorPositiveRun	:	BOOL;    //电梯处于向上运动状态
	QMotorNegativeRun	:	BOOL; //电梯处于向下运动状态
	QClose	:	BOOL := TRUE;    //电梯是处于关闭状态
	QOpen	:	BOOL;               //电梯是处于打开状态
	QHelpBeer	:	BOOL;        //报警灯是亮还是灭
	
	QGoFloorLed	:	ARRAY[1..MaxNumFloor] OF BOOL;   //电梯内“1/2/3/4”按钮，为TRUE时，按钮亮

	QFloorUpLed	:	ARRAY[1..MaxNumFloor - 1] OF BOOL;   //楼层中3个“上”按钮，为TRUE时，按钮亮
	QFloorDownLed	:	ARRAY[2..MaxNumFloor] OF BOOL;   //楼层中3个“下”按钮，为TRUE时，按钮亮
END_VAR
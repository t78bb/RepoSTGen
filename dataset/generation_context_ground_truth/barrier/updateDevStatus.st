VAR
	extendVal	:REAL;		//伸出值
	retractVal	:REAL;		//缩回到位值
	nowVal		:REAL;		//当前值
	stat		:DevStatus;	//设备状态
END_VAR

(* 本函数用于根据设备的标定伸出/缩回值以及当前位置
** 判断该缸体是否处于伸出/缩回到位状态，如果到位更新参数
*)

stat := DevStatus.unknown;	//初始化状态量
CASE level OF
	1:
		extendVal := gDev.grd[idx].sensor.extendVal;
		retractVal := gDev.grd[idx].sensor.retractVal;
		nowVal := gDev.grd[idx].sensor.position;
		stat := gDev.grd[idx].state;
	2:
		extendVal := gDev.sky[idx].sensor.extendVal;
		retractVal := gDev.sky[idx].sensor.retractVal;
		nowVal := gDev.sky[idx].sensor.position;
		stat := gDev.sky[idx].state;
END_CASE

IF nowVal > 1 THEN
	IF nowVal < retractVal + errorVal THEN
		stat := DevStatus.retracted;
	ELSIF nowVal > extendVal - errorVal THEN
		stat := DevStatus.extended;
	ELSE 
		IF stat <> DevStatus.runing THEN
			stat := DevStatus.error;
		END_IF
	END_IF
ELSE
	stat := DevStatus.unknown;	
END_IF

CASE level OF
	1:
		gDev.grd[idx].state := stat;
	2:
		gDev.sky[idx].state := stat;
END_CASE

updateDevStatus := stat;
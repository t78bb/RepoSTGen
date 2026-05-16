TYPE UIMode :
STRUCT
	manualButtonSet			:BOOL;		//手动复位按钮模式
	usePID					:BOOL;		//使用pid
	autoEnable				:BOOL;		//自动使能
	manualPercentSet		:BOOL;		//手动设定比例量
	manualSetPid			:BOOL;		//手动调节pid参数，可通过pid测试界面设定目标位移值
	
	syncExt					:BOOL;		//同步伸
	syncRct					:BOOL;		//同步缩
	
	hydPowerOn				:BOOL;		//液压站开启 modbus 使用
	hydPowerOff				:BOOL;		//液压站关闭 modbus 使用
	hydPowerReset			:BOOL;		
END_STRUCT
END_TYPE

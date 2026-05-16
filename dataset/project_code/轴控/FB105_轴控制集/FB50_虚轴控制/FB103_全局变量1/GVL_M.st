VAR_GLOBAL
	b所有伺服总线通讯OK: BOOL;
	b所有伺服使能OK: BOOL;
	b所有伺服回零OK: BOOL;
	b所有伺服静止中: BOOL;
	b所有气缸原位OK: BOOL;
	b所有气缸关闭OK: BOOL;
		
	b开机初始化: BOOL;
	b常闭: BOOL := TRUE;
	b常开: BOOL := FALSE;
	b非急停手动模式: BOOL;	
	b非急停自动模式: BOOL;
	
	b开机第一次启动: BOOL;
	b常通: BOOL;
	
	b自动运行: BOOL;
	b自动互锁: BOOL;
	b设备初始化中: BOOL;
	b轴控初始化: BOOL;
	b设备报警: BOOL;
	b气缸报警: BOOL;
	b真空报警: BOOL;
	b马达报警: BOOL;
	b其它报警: BOOL;

END_VAR
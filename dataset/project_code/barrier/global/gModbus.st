{attribute 'qualified_only'}
VAR_GLOBAL CONSTANT
	g_modbusDataSizeMax	:  UINT:=65535; // 从机保持寄存器数量
END_VAR
VAR_GLOBAL
	srv				:mdbsStruct;		//modbus-service
	modbusBuffer	:ARRAY[0..g_modbusDataSizeMax] OF WORD;	//输入寄存器数据区	
END_VAR

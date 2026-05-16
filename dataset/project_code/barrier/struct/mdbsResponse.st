TYPE mdbsResponse :	//所有响应状态数据回送
STRUCT
	startAddr		:WORD;							//解析起始地址->110
	length			:WORD;							//字节长度->210
	
	data			:ARRAY[110..319] OF WORD;		//位置数据

END_STRUCT
END_TYPE

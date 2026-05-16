TYPE mdbsRequest :	//所有请求动作指令数据
STRUCT
	startAddr		:WORD;					//解析起始地址->10
	length			:WORD;					//数据长度/字节->48
	data			:ARRAY[10..57] OF WORD;	//指令数据	
	
	arrNew		:ARRAY [1..4,0..15] OF BOOL;
	arrLast		:ARRAY [1..4,0..15] OF BOOL;

END_STRUCT
END_TYPE

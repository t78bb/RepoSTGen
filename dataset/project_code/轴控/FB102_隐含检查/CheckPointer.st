// 隐式生成代码:不需要编辑
FUNCTION CheckPointer : POINTER TO BYTE
VAR_INPUT 
	ptToTest : POINTER TO BYTE; // 指针的目标地址
	iSize : DINT;		         //指针指向的类型大小.(例如:POINTER TO ARRAY [0..9] OF INT为20)
	iGran : DINT;		        // 指针访问的粒度,即指针指向的类型中最大的非结构数据类型的大小.(例如: POINTER TO ARRAY [0..9] OF INT为2)
	bWrite: BOOL;		        // 标识读或写权限.TRUE = 写权限.
END_VAR

// 没有标准的实现方式.在此处输入代码
CheckPointer := ptToTest;
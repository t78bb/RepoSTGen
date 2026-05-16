VAR_GLOBAL
	FB_AxisControl_折边轴: FB_轴控块;

//轴触发类		 
	b折边轴正向点动: BOOL;
	b折边轴反向点动: BOOL;
	b折边轴正向寸动: BOOL;
	b折边轴反向寸动: BOOL;	
	b折边轴停止触发: BOOL;
	b折边轴复位触发: BOOL;	
	b折边轴绝对运动触发: BOOL;
	b折边轴相对运动触发: BOOL;
	b折边轴速度模式触发: BOOL;
	b折边轴启用限位: BOOL;

//轴状态类	
    b折边轴通讯OK: BOOL;
	b折边轴使能OK: BOOL; 
	b折边轴停止完成: BOOL; 
	b折边轴绝对运动完成: BOOL; 
	b折边轴相对运动完成: BOOL; 
	b折边轴速度模式Busy: BOOL;
	b折边轴寸动模式Busy: BOOL;
	b折边轴点动模式Busy: BOOL;
	b折边轴绝对模式Busy: BOOL;
	b折边轴相对模式Busy: BOOL;
	b折边轴错误: BOOL;
	b折边轴加速中: BOOL;
	b折边轴减速中: BOOL;
    b折边轴停止中: BOOL;

//数据给定类
	r折边轴点动速度给定: LREAL;
	r折边轴绝对运动速度给定: LREAL;
	r折边轴相对运动速度给定: LREAL;
	r折边轴速度模式速度给定: LREAL;
	r折边轴寸动速度给定: LREAL;
	
	r折边轴绝对运动位置给定: LREAL;		
	r折边轴相对运动位置给定: LREAL;
	r折边轴寸动位置给定: LREAL;
		
//数据读取类	
    r折边轴当前位置: LREAL;
	r折边轴当前速度: LREAL;
	r折边轴当前扭矩: LREAL;
	
//其它类
    b折边轴回零触发: BOOL; 
    b折边轴回零Busy: BOOL; 
    b折边轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b折边轴断使能	AT %MX360.0: BOOL;
	HMI_b折边轴单独回原	AT %MX360.1: BOOL;
	HMI_b折边轴正向点动	AT %MX360.2: BOOL;
    HMI_b折边轴反向点动	AT %MX360.3: BOOL;
	
	HMI_b折边轴设为原点	AT %MX360.4: BOOL;
	HMI_b折边轴去停料位	AT %MX360.5: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL	
	HMI_r折边轴当前位置 	AT %MD16200: REAL;
	HMI_r折边轴当前速度 	AT %MD16201: REAL;
	HMI_r折边轴自动速度 	AT %MD16202: REAL;
	HMI_r折边轴手动速度 	AT %MD16203: REAL;
	
	HMI_r折边轴导程 		AT %MD16204: REAL;
	HMI_r折边轴齿轮比分子 	AT %MD16205: REAL;
	HMI_r折边轴齿轮比分母 	AT %MD16206: REAL;
	
	HMI_r折边轴回零快速 	AT %MD16207: REAL;
	HMI_r折边轴回零慢速 	AT %MD16208: REAL;
	HMI_r折边轴正限位 		AT %MD16209: REAL;
	HMI_r折边轴负限位 		AT %MD16210: REAL;
	
	HMI_r折边轴加速时间 	AT %MD16211: REAL;
	HMI_r折边轴减速时间 	AT %MD16212: REAL;
	
	HMI_r折边轴停料位 		AT %MD16213: REAL;
END_VAR



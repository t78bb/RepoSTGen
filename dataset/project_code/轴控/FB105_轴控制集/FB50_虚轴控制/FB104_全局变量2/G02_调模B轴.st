VAR_GLOBAL
	FB_AxisControl_调模B轴: FB_轴控块;

//轴触发类		 
	b调模B轴正向点动: BOOL;
	b调模B轴反向点动: BOOL;
	b调模B轴正向寸动: BOOL;
	b调模B轴反向寸动: BOOL;	
	b调模B轴停止触发: BOOL;
	b调模B轴复位触发: BOOL;	
	b调模B轴绝对运动触发: BOOL;
	b调模B轴相对运动触发: BOOL;
	b调模B轴速度模式触发: BOOL;
	b调模B轴启用限位: BOOL;

//轴状态类	
    b调模B轴通讯OK: BOOL;
	b调模B轴使能OK: BOOL; 
	b调模B轴停止完成: BOOL; 
	b调模B轴绝对运动完成: BOOL; 
	b调模B轴相对运动完成: BOOL; 
	b调模B轴速度模式Busy: BOOL;
	b调模B轴寸动模式Busy: BOOL;
	b调模B轴点动模式Busy: BOOL;
	b调模B轴绝对模式Busy: BOOL;
	b调模B轴相对模式Busy: BOOL;
	b调模B轴错误: BOOL;
	b调模B轴加速中: BOOL;
	b调模B轴减速中: BOOL;
    b调模B轴停止中: BOOL;

//数据给定类
	r调模B轴点动速度给定: LREAL;
	r调模B轴绝对运动速度给定: LREAL;
	r调模B轴相对运动速度给定: LREAL;
	r调模B轴速度模式速度给定: LREAL;
	r调模B轴寸动速度给定: LREAL;
	
	r调模B轴绝对运动位置给定: LREAL;		
	r调模B轴相对运动位置给定: LREAL;
	r调模B轴寸动位置给定: LREAL;
		
//数据读取类	
    r调模B轴当前位置: LREAL;
	r调模B轴当前速度: LREAL;
	r调模B轴当前扭矩: LREAL;
	
//其它类
    b调模B轴回零触发: BOOL; 
    b调模B轴回零Busy: BOOL; 
    b调模B轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b调模B轴断使能 	 AT %MX305.0: BOOL;
	HMI_b调模B轴单独回原 AT %MX305.1: BOOL;
	HMI_b调模B轴正向点动 AT %MX305.2: BOOL;
    HMI_b调模B轴反向点动 AT %MX305.3: BOOL;
	
	HMI_b调模B轴去工作位 AT %MX305.4: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL
	HMI_r调模B轴当前位置 	AT %MD15650: REAL;
	HMI_r调模B轴当前速度 	AT %MD15651: REAL;
	HMI_r调模B轴自动速度 	AT %MD15652: REAL;
	HMI_r调模B轴手动速度 	AT %MD15653: REAL;
	
	HMI_r调模B轴导程 		AT %MD15654: REAL;
	HMI_r调模B轴齿轮比分子 	AT %MD15655: REAL;
	HMI_r调模B轴齿轮比分母 	AT %MD15656: REAL;
	
	HMI_r调模B轴回零快速 	AT %MD15657: REAL;
	HMI_r调模B轴回零慢速 	AT %MD15658: REAL;
	HMI_r调模B轴正限位 		AT %MD15659: REAL;
	HMI_r调模B轴负限位 		AT %MD15660: REAL;
	
	HMI_r调模B轴加速时间 	AT %MD15661: REAL;
	HMI_r调模B轴减速时间 	AT %MD15662: REAL;
	
	HMI_r调模B轴宽度位置 	AT %MD15663: REAL;
END_VAR



VAR_GLOBAL
	FB_AxisControl_升降A轴: FB_轴控块;

//轴触发类		 
	b升降A轴正向点动: BOOL;
	b升降A轴反向点动: BOOL;
	b升降A轴正向寸动: BOOL;
	b升降A轴反向寸动: BOOL;	
	b升降A轴停止触发: BOOL;
	b升降A轴复位触发: BOOL;	
	b升降A轴绝对运动触发: BOOL;
	b升降A轴相对运动触发: BOOL;
	b升降A轴速度模式触发: BOOL;
	b升降A轴启用限位: BOOL;

//轴状态类	
    b升降A轴通讯OK: BOOL;
	b升降A轴使能OK: BOOL; 
	b升降A轴停止完成: BOOL; 
	b升降A轴绝对运动完成: BOOL; 
	b升降A轴相对运动完成: BOOL; 
	b升降A轴速度模式Busy: BOOL;
	b升降A轴寸动模式Busy: BOOL;
	b升降A轴点动模式Busy: BOOL;
	b升降A轴绝对模式Busy: BOOL;
	b升降A轴相对模式Busy: BOOL;
	b升降A轴错误: BOOL;
	b升降A轴加速中: BOOL;
	b升降A轴减速中: BOOL;
    b升降A轴停止中: BOOL;

//数据给定类
	r升降A轴点动速度给定: LREAL;
	r升降A轴绝对运动速度给定: LREAL;
	r升降A轴相对运动速度给定: LREAL;
	r升降A轴速度模式速度给定: LREAL;
	r升降A轴寸动速度给定: LREAL;
	
	r升降A轴绝对运动位置给定: LREAL;		
	r升降A轴相对运动位置给定: LREAL;
	r升降A轴寸动位置给定: LREAL;
		
//数据读取类	
    r升降A轴当前位置: LREAL;
	r升降A轴当前速度: LREAL;
	r升降A轴当前扭矩: LREAL;
	
//其它类
    b升降A轴回零触发: BOOL; 
    b升降A轴回零Busy: BOOL; 
    b升降A轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b升降A轴断使能 	 AT %MX325.0: BOOL;
	HMI_b升降A轴单独回原 AT %MX325.1: BOOL;
	HMI_b升降A轴正向点动 AT %MX325.2: BOOL;
    HMI_b升降A轴反向点动 AT %MX325.3: BOOL;
	
	HMI_b升降A轴设为原点 AT %MX325.4: BOOL;
	HMI_b升降A轴去接底板位 	 AT %MX325.5: BOOL;
	HMI_b升降A轴去接面位 	 AT %MX325.6: BOOL;
	HMI_b升降A轴去成型位 	 AT %MX325.7: BOOL;
	HMI_b升降A轴去出料位 	 AT %MX326.0: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL
	HMI_r升降A轴当前位置 	AT %MD15850: REAL;
	HMI_r升降A轴当前速度 	AT %MD15851: REAL;
	HMI_r升降A轴自动速度 	AT %MD15852: REAL;
	HMI_r升降A轴手动速度 	AT %MD15853: REAL;
	
	HMI_r升降A轴导程 		AT %MD15854: REAL;
	HMI_r升降A轴齿轮比分子 	AT %MD15855: REAL;
	HMI_r升降A轴齿轮比分母 	AT %MD15856: REAL;
	
	HMI_r升降A轴回零快速 	AT %MD15857: REAL;
	HMI_r升降A轴回零慢速 	AT %MD15858: REAL;
	HMI_r升降A轴正限位 		AT %MD15859: REAL;
	HMI_r升降A轴负限位 		AT %MD15860: REAL;

	HMI_r升降A轴加速时间 	AT %MD15861: REAL;
	HMI_r升降A轴减速时间 	AT %MD15862: REAL;
	
	HMI_r升降A轴接底板位 	AT %MD15863: REAL;
	HMI_r升降A轴接面位 		AT %MD15864: REAL;
	HMI_r升降A轴成型位 		AT %MD15865: REAL;	
	HMI_r升降A轴出料位 		AT %MD15866: REAL;

END_VAR



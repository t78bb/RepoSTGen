VAR_GLOBAL
	FB_AxisControl_取面料轴: FB_轴控块;

//轴触发类		 
	b取面料轴正向点动: BOOL;
	b取面料轴反向点动: BOOL;
	b取面料轴正向寸动: BOOL;
	b取面料轴反向寸动: BOOL;	
	b取面料轴停止触发: BOOL;
	b取面料轴复位触发: BOOL;	
	b取面料轴绝对运动触发: BOOL;
	b取面料轴相对运动触发: BOOL;
	b取面料轴速度模式触发: BOOL;
	b取面料轴启用限位: BOOL;

//轴状态类	
    b取面料轴通讯OK: BOOL;
	b取面料轴使能OK: BOOL; 
	b取面料轴停止完成: BOOL; 
	b取面料轴绝对运动完成: BOOL; 
	b取面料轴相对运动完成: BOOL; 
	b取面料轴速度模式Busy: BOOL;
	b取面料轴寸动模式Busy: BOOL;
	b取面料轴点动模式Busy: BOOL;
	b取面料轴绝对模式Busy: BOOL;
	b取面料轴相对模式Busy: BOOL;
	b取面料轴错误: BOOL;
	b取面料轴加速中: BOOL;
	b取面料轴减速中: BOOL;
    b取面料轴停止中: BOOL;

//数据给定类
	r取面料轴点动速度给定: LREAL;
	r取面料轴绝对运动速度给定: LREAL;
	r取面料轴相对运动速度给定: LREAL;
	r取面料轴速度模式速度给定: LREAL;
	r取面料轴寸动速度给定: LREAL;
	
	r取面料轴绝对运动位置给定: LREAL;		
	r取面料轴相对运动位置给定: LREAL;
	r取面料轴寸动位置给定: LREAL;
		
//数据读取类	
    r取面料轴当前位置: LREAL;
	r取面料轴当前速度: LREAL;
	r取面料轴当前扭矩: LREAL;
	
//其它类
    b取面料轴回零触发: BOOL; 
    b取面料轴回零Busy: BOOL; 
    b取面料轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b取面料轴断使能 	 AT %MX315.0: BOOL;
	HMI_b取面料轴单独回原 	 AT %MX315.1: BOOL;
	HMI_b取面料轴正向点动 	 AT %MX315.2: BOOL;
    HMI_b取面料轴反向点动 	 AT %MX315.3: BOOL;
	
	HMI_b取面料轴设为原点 	 AT %MX315.4: BOOL;
	HMI_b取面料轴去取料位 	 AT %MX315.5: BOOL;
	HMI_b取面料轴去等待位 	 AT %MX315.6: BOOL;
	HMI_b取面料轴去送料位 	 AT %MX315.7: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL	
	HMI_r取面料轴当前位置 	AT %MD15750: REAL;
	HMI_r取面料轴当前速度 	AT %MD15751: REAL;
	HMI_r取面料轴自动速度 	AT %MD15752: REAL;
	HMI_r取面料轴手动速度 	AT %MD15753: REAL;
	
	HMI_r取面料轴导程 		AT %MD15754: REAL;
	HMI_r取面料轴齿轮比分子 AT %MD15755: REAL;
	HMI_r取面料轴齿轮比分母 AT %MD15756: REAL;
	
	HMI_r取面料轴回零快速 	AT %MD15757: REAL;
	HMI_r取面料轴回零慢速 	AT %MD15758: REAL;
	HMI_r取面料轴正限位 	AT %MD15759: REAL;
	HMI_r取面料轴负限位 	AT %MD15760: REAL;
	
	HMI_r取面料轴加速时间 	AT %MD15761: REAL;
	HMI_r取面料轴减速时间 	AT %MD15762: REAL;
	
	HMI_r取面料轴取料位 	AT %MD15763: REAL;
	HMI_r取面料轴等待位 	AT %MD15764: REAL;
	HMI_r取面料轴送料位 	AT %MD15765: REAL;
	
END_VAR



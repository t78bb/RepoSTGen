VAR_GLOBAL
	FB_AxisControl_升降B轴: FB_轴控块;

//轴触发类		 
	b升降B轴正向点动: BOOL;
	b升降B轴反向点动: BOOL;
	b升降B轴正向寸动: BOOL;
	b升降B轴反向寸动: BOOL;	
	b升降B轴停止触发: BOOL;
	b升降B轴复位触发: BOOL;	
	b升降B轴绝对运动触发: BOOL;
	b升降B轴相对运动触发: BOOL;
	b升降B轴速度模式触发: BOOL;
	b升降B轴启用限位: BOOL;

//轴状态类	
    b升降B轴通讯OK: BOOL;
	b升降B轴使能OK: BOOL; 
	b升降B轴停止完成: BOOL; 
	b升降B轴绝对运动完成: BOOL; 
	b升降B轴相对运动完成: BOOL; 
	b升降B轴速度模式Busy: BOOL;
	b升降B轴寸动模式Busy: BOOL;
	b升降B轴点动模式Busy: BOOL;
	b升降B轴绝对模式Busy: BOOL;
	b升降B轴相对模式Busy: BOOL;
	b升降B轴错误: BOOL;
	b升降B轴加速中: BOOL;
	b升降B轴减速中: BOOL;
    b升降B轴停止中: BOOL;

//数据给定类
	r升降B轴点动速度给定: LREAL;
	r升降B轴绝对运动速度给定: LREAL;
	r升降B轴相对运动速度给定: LREAL;
	r升降B轴速度模式速度给定: LREAL;
	r升降B轴寸动速度给定: LREAL;
	
	r升降B轴绝对运动位置给定: LREAL;		
	r升降B轴相对运动位置给定: LREAL;
	r升降B轴寸动位置给定: LREAL;
		
//数据读取类	
    r升降B轴当前位置: LREAL;
	r升降B轴当前速度: LREAL;
	r升降B轴当前扭矩: LREAL;
	
//其它类
    b升降B轴回零触发: BOOL; 
    b升降B轴回零Busy: BOOL; 
    b升降B轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b升降B轴断使能 	 		AT %MX335.0: BOOL;
	HMI_b升降B轴单独回原 		AT %MX335.1: BOOL;
	HMI_b升降B轴正向点动 	 	AT %MX335.2: BOOL;
    HMI_b升降B轴反向点动 	 	AT %MX335.3: BOOL;
	
	HMI_b升降B轴设为原点 	 	AT %MX335.4: BOOL;
	HMI_b升降B轴去接底板位 	 	AT %MX335.5: BOOL;
	HMI_b升降B轴去接面位 	 	AT %MX335.6: BOOL;
	HMI_b升降B轴去成型位 	 	AT %MX335.7: BOOL;
	HMI_b升降B轴去出料位 	 	AT %MX336.0: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL
	HMI_r升降B轴当前位置 	AT %MD15950: REAL;
	HMI_r升降B轴当前速度 	AT %MD15951: REAL;
	HMI_r升降B轴自动速度 	AT %MD15952: REAL;
	HMI_r升降B轴手动速度 	AT %MD15953: REAL;
	
	HMI_r升降B轴导程 		AT %MD15954: REAL;
	HMI_r升降B轴齿轮比分子 	AT %MD15955: REAL;
	HMI_r升降B轴齿轮比分母 	AT %MD15956: REAL;
	
	HMI_r升降B轴回零快速 	AT %MD15957: REAL;
	HMI_r升降B轴回零慢速 	AT %MD15958: REAL;
	HMI_r升降B轴正限位 		AT %MD15959: REAL;
	HMI_r升降B轴负限位 		AT %MD15960: REAL;
	
	HMI_r升降B轴加速时间 	AT %MD15961: REAL;
	HMI_r升降B轴减速时间 	AT %MD15962: REAL;
	
	HMI_r升降B轴接底板位 	AT %MD15963: REAL;
	HMI_r升降B轴接面位 		AT %MD15964: REAL;
	HMI_r升降B轴成型位 		AT %MD15965: REAL;	
	HMI_r升降B轴出料位 		AT %MD15966: REAL;
END_VAR



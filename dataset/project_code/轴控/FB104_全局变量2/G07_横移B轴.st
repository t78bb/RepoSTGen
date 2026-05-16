VAR_GLOBAL
	FB_AxisControl_横移B轴: FB_轴控块;

//轴触发类		 
	b横移B轴正向点动: BOOL;
	b横移B轴反向点动: BOOL;
	b横移B轴正向寸动: BOOL;
	b横移B轴反向寸动: BOOL;	
	b横移B轴停止触发: BOOL;
	b横移B轴复位触发: BOOL;	
	b横移B轴绝对运动触发: BOOL;
	b横移B轴相对运动触发: BOOL;
	b横移B轴速度模式触发: BOOL;
	b横移B轴启用限位: BOOL;

//轴状态类	
    b横移B轴通讯OK: BOOL;
	b横移B轴使能OK: BOOL; 
	b横移B轴停止完成: BOOL; 
	b横移B轴绝对运动完成: BOOL; 
	b横移B轴相对运动完成: BOOL; 
	b横移B轴速度模式Busy: BOOL;
	b横移B轴寸动模式Busy: BOOL;
	b横移B轴点动模式Busy: BOOL;
	b横移B轴绝对模式Busy: BOOL;
	b横移B轴相对模式Busy: BOOL;
	b横移B轴错误: BOOL;
	b横移B轴加速中: BOOL;
	b横移B轴减速中: BOOL;
    b横移B轴停止中: BOOL;

//数据给定类
	r横移B轴点动速度给定: LREAL;
	r横移B轴绝对运动速度给定: LREAL;
	r横移B轴相对运动速度给定: LREAL;
	r横移B轴速度模式速度给定: LREAL;
	r横移B轴寸动速度给定: LREAL;
	
	r横移B轴绝对运动位置给定: LREAL;		
	r横移B轴相对运动位置给定: LREAL;
	r横移B轴寸动位置给定: LREAL;
		
//数据读取类	
    r横移B轴当前位置: LREAL;
	r横移B轴当前速度: LREAL;
	r横移B轴当前扭矩: LREAL;
	
//其它类
    b横移B轴回零触发: BOOL; 
    b横移B轴回零Busy: BOOL; 
    b横移B轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b横移B轴断使能 	 	 AT %MX330.0: BOOL;
	HMI_b横移B轴单独回原 	 AT %MX330.1: BOOL;
	HMI_b横移B轴正向点动 	 AT %MX330.2: BOOL;
    HMI_b横移B轴反向点动 	 AT %MX330.3: BOOL;
	
	HMI_b横移B轴设为原点 	 AT %MX330.4: BOOL;
	HMI_b横移B轴去接底板位 	 AT %MX330.5: BOOL;
	HMI_b横移B轴去成型位 	 AT %MX330.6: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL
	HMI_r横移B轴当前位置 	AT %MD15900: REAL;
	HMI_r横移B轴当前速度 	AT %MD15901: REAL;
	HMI_r横移B轴自动速度 	AT %MD15902: REAL;
	HMI_r横移B轴手动速度 	AT %MD15903: REAL;
	
	HMI_r横移B轴导程 		AT %MD15904: REAL;
	HMI_r横移B轴齿轮比分子 	AT %MD15905: REAL;
	HMI_r横移B轴齿轮比分母 	AT %MD15906: REAL;
	
	HMI_r横移B轴回零快速 	AT %MD15907: REAL;
	HMI_r横移B轴回零慢速 	AT %MD15908: REAL;
	HMI_r横移B轴正限位 		AT %MD15909: REAL;
	HMI_r横移B轴负限位 		AT %MD15910: REAL;
	
	HMI_r横移B轴加速时间 	AT %MD15911: REAL;
	HMI_r横移B轴减速时间 	AT %MD15912: REAL;
	
	HMI_r横移B轴接底板位 	AT %MD15913: REAL;
	HMI_r横移B轴成型位 		AT %MD15914: REAL;
	
	
END_VAR



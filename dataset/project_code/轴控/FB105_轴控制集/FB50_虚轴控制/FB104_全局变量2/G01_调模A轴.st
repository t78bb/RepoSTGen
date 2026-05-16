VAR_GLOBAL
	FB_AxisControl_调模A轴: FB_轴控块;

//轴触发类		 
	b调模A轴正向点动: BOOL;
	b调模A轴反向点动: BOOL;
	b调模A轴正向寸动: BOOL;
	b调模A轴反向寸动: BOOL;	
	b调模A轴停止触发: BOOL;
	b调模A轴复位触发: BOOL;	
	b调模A轴绝对运动触发: BOOL;
	b调模A轴相对运动触发: BOOL;
	b调模A轴速度模式触发: BOOL;
	b调模A轴启用限位: BOOL;

//轴状态类	
    b调模A轴通讯OK: BOOL;
	b调模A轴使能OK: BOOL; 
	b调模A轴停止完成: BOOL; 
	b调模A轴绝对运动完成: BOOL; 
	b调模A轴相对运动完成: BOOL; 
	b调模A轴速度模式Busy: BOOL;
	b调模A轴寸动模式Busy: BOOL;
	b调模A轴点动模式Busy: BOOL;
	b调模A轴绝对模式Busy: BOOL;
	b调模A轴相对模式Busy: BOOL;
	b调模A轴错误: BOOL;
	b调模A轴加速中: BOOL;
	b调模A轴减速中: BOOL;
    b调模A轴停止中: BOOL;

//数据给定类
	r调模A轴点动速度给定: LREAL;
	r调模A轴绝对运动速度给定: LREAL;
	r调模A轴相对运动速度给定: LREAL;
	r调模A轴速度模式速度给定: LREAL;
	r调模A轴寸动速度给定: LREAL;
	
	r调模A轴绝对运动位置给定: LREAL;		
	r调模A轴相对运动位置给定: LREAL;
	r调模A轴寸动位置给定: LREAL;
		
//数据读取类	
    r调模A轴当前位置: LREAL;
	r调模A轴当前速度: LREAL;
	r调模A轴当前扭矩: LREAL;
	
//其它类
    b调模A轴回零触发: BOOL; 
    b调模A轴回零Busy: BOOL; 
    b调模A轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b调模A轴断使能 	 AT %MX300.0: BOOL;
	HMI_b调模A轴单独回原 AT %MX300.1: BOOL;
	HMI_b调模A轴正向点动 AT %MX300.2: BOOL;
    HMI_b调模A轴反向点动 AT %MX300.3: BOOL;
	
	HMI_b调模A轴去工作位 AT %MX300.4: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL PERSISTENT RETAIN	
	HMI_r调模A轴当前位置 	AT %MD15600: REAL;
	HMI_r调模A轴当前速度 	AT %MD15601: REAL;
	HMI_r调模A轴自动速度 	AT %MD15602: REAL;
	HMI_r调模A轴手动速度 	AT %MD15603: REAL;
	
	HMI_r调模A轴导程 		AT %MD15604: REAL;
	HMI_r调模A轴齿轮比分子 	AT %MD15605: REAL;
	HMI_r调模A轴齿轮比分母 	AT %MD15606: REAL;
	
	HMI_r调模A轴回零快速 	AT %MD15607: REAL;
	HMI_r调模A轴回零慢速 	AT %MD15608: REAL;
	HMI_r调模A轴正限位 		AT %MD15609: REAL;
	HMI_r调模A轴负限位 		AT %MD15610: REAL;
	
	HMI_r调模A轴加速时间 	AT %MD15611: REAL;
	HMI_r调模A轴减速时间 	AT %MD15612: REAL;
	
	HMI_r调模A轴宽度位置 	AT %MD15613: REAL;

END_VAR



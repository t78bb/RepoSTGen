VAR_GLOBAL
	FB_AxisControl_送面料轴: FB_轴控块;

//轴触发类		 
	b送面料轴正向点动: BOOL;
	b送面料轴反向点动: BOOL;
	b送面料轴正向寸动: BOOL;
	b送面料轴反向寸动: BOOL;	
	b送面料轴停止触发: BOOL;
	b送面料轴复位触发: BOOL;	
	b送面料轴绝对运动触发: BOOL;
	b送面料轴相对运动触发: BOOL;
	b送面料轴速度模式触发: BOOL;
	b送面料轴启用限位: BOOL;

//轴状态类	
    b送面料轴通讯OK: BOOL;
	b送面料轴使能OK: BOOL; 
	b送面料轴停止完成: BOOL; 
	b送面料轴绝对运动完成: BOOL; 
	b送面料轴相对运动完成: BOOL; 
	b送面料轴速度模式Busy: BOOL;
	b送面料轴寸动模式Busy: BOOL;
	b送面料轴点动模式Busy: BOOL;
	b送面料轴绝对模式Busy: BOOL;
	b送面料轴相对模式Busy: BOOL;
	b送面料轴错误: BOOL;
	b送面料轴加速中: BOOL;
	b送面料轴减速中: BOOL;
    b送面料轴停止中: BOOL;

//数据给定类
	r送面料轴点动速度给定: LREAL;
	r送面料轴绝对运动速度给定: LREAL;
	r送面料轴相对运动速度给定: LREAL;
	r送面料轴速度模式速度给定: LREAL;
	r送面料轴寸动速度给定: LREAL;
	
	r送面料轴绝对运动位置给定: LREAL;		
	r送面料轴相对运动位置给定: LREAL;
	r送面料轴寸动位置给定: LREAL;
		
//数据读取类	
    r送面料轴当前位置: LREAL;
	r送面料轴当前速度: LREAL;
	r送面料轴当前扭矩: LREAL;
	
//其它类
    b送面料轴回零触发: BOOL; 
    b送面料轴回零Busy: BOOL; 
    b送面料轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b送面料轴断使能 	 AT %MX310.0: BOOL;
	HMI_b送面料轴单独回原 	 AT %MX310.1: BOOL;
	HMI_b送面料轴正向点动 	 AT %MX310.2: BOOL;
    HMI_b送面料轴反向点动 	 AT %MX310.3: BOOL;
	
	HMI_b送面料轴设为原点 	 AT %MX310.4: BOOL;
	
	HMI_b送面料轴去停料位 	 	 AT %MX310.5: BOOL;
	HMI_b送面料轴去停料位保存 	 AT %MX310.6: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL
	HMI_r送面料轴当前位置 : REAL;
	HMI_r送面料轴当前速度 	AT %MD15700: REAL;
	HMI_r送面料轴自动速度 	AT %MD15701: REAL;
	HMI_r送面料轴手动速度 	AT %MD15702: REAL;
	
	HMI_r送面料轴导程 		AT %MD15703: REAL;
	HMI_r送面料轴齿轮比分子 AT %MD15704: REAL;
	HMI_r送面料轴齿轮比分母 AT %MD15705: REAL;
	
	HMI_r送面料轴回零快速 	AT %MD15706: REAL;
	HMI_r送面料轴回零慢速 	AT %MD15707: REAL;
	HMI_r送面料轴正限位 	AT %MD15708: REAL;
	HMI_r送面料轴负限位 	AT %MD15709: REAL;
	
	HMI_r送面料轴加速时间 	AT %MD15710: REAL;
	HMI_r送面料轴减速时间 	AT %MD15711: REAL;
	
	HMI_r送面料轴定位走距离长度 AT %MD15712: REAL;
	HMI_r送面料轴停料位 		AT %MD15713: REAL;
	
END_VAR



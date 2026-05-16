VAR_GLOBAL
	FB_AxisControl_出盒轴: FB_轴控块;

//轴触发类		 
	b出盒轴正向点动: BOOL;
	b出盒轴反向点动: BOOL;
	b出盒轴正向寸动: BOOL;
	b出盒轴反向寸动: BOOL;	
	b出盒轴停止触发: BOOL;
	b出盒轴复位触发: BOOL;	
	b出盒轴绝对运动触发: BOOL;
	b出盒轴相对运动触发: BOOL;
	b出盒轴速度模式触发: BOOL;
	b出盒轴启用限位: BOOL;

//轴状态类	
    b出盒轴通讯OK: BOOL;
	b出盒轴使能OK: BOOL; 
	b出盒轴停止完成: BOOL; 
	b出盒轴绝对运动完成: BOOL; 
	b出盒轴相对运动完成: BOOL; 
	b出盒轴速度模式Busy: BOOL;
	b出盒轴寸动模式Busy: BOOL;
	b出盒轴点动模式Busy: BOOL;
	b出盒轴绝对模式Busy: BOOL;
	b出盒轴相对模式Busy: BOOL;
	b出盒轴错误: BOOL;
	b出盒轴加速中: BOOL;
	b出盒轴减速中: BOOL;
    b出盒轴停止中: BOOL;

//数据给定类
	r出盒轴点动速度给定: LREAL;
	r出盒轴绝对运动速度给定: LREAL;
	r出盒轴相对运动速度给定: LREAL;
	r出盒轴速度模式速度给定: LREAL;
	r出盒轴寸动速度给定: LREAL;
	
	r出盒轴绝对运动位置给定: LREAL;		
	r出盒轴相对运动位置给定: LREAL;
	r出盒轴寸动位置给定: LREAL;
		
//数据读取类	
    r出盒轴当前位置: LREAL;
	r出盒轴当前速度: LREAL;
	r出盒轴当前扭矩: LREAL;
	
//其它类
    b出盒轴回零触发: BOOL; 
    b出盒轴回零Busy: BOOL; 
    b出盒轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b出盒轴断使能	AT %MX340.0: BOOL;
	HMI_b出盒轴单独回原	AT %MX340.1: BOOL;
	HMI_b出盒轴正向点动	AT %MX340.2: BOOL;
    HMI_b出盒轴反向点动	AT %MX340.3: BOOL;
	
	HMI_b出盒轴设为原点	AT %MX340.4: BOOL;
	HMI_b出盒轴去待料位	AT %MX340.5: BOOL;
	HMI_b出盒轴去出盒位	AT %MX340.6: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL	
	HMI_r出盒轴当前位置 	AT %MD16000: REAL;
	HMI_r出盒轴当前速度		AT %MD16001: REAL;
	HMI_r出盒轴自动速度 	AT %MD16002: REAL;
	HMI_r出盒轴手动速度 	AT %MD16003: REAL;
	
	HMI_r出盒轴导程 		AT %MD16004: REAL;
	HMI_r出盒轴齿轮比分子 	AT %MD16005: REAL;
	HMI_r出盒轴齿轮比分母 	AT %MD16006: REAL;
	
	HMI_r出盒轴回零快速 	AT %MD16007: REAL;
	HMI_r出盒轴回零慢速 	AT %MD16008: REAL;
	HMI_r出盒轴正限位 		AT %MD16009: REAL;
	HMI_r出盒轴负限位 		AT %MD16010: REAL;
	
	HMI_r出盒轴加速时间 	AT %MD16011: REAL;
	HMI_r出盒轴减速时间 	AT %MD16012: REAL;

	HMI_r出盒轴待料位 		AT %MD16013: REAL;
	HMI_r出盒轴出盒位 		AT %MD16014: REAL;

END_VAR



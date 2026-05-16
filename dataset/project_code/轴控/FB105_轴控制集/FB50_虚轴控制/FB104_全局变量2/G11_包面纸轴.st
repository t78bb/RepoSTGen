VAR_GLOBAL
	FB_AxisControl_包面纸轴: FB_轴控块;

//轴触发类		 
	b包面纸轴正向点动: BOOL;
	b包面纸轴反向点动: BOOL;
	b包面纸轴正向寸动: BOOL;
	b包面纸轴反向寸动: BOOL;	
	b包面纸轴停止触发: BOOL;
	b包面纸轴复位触发: BOOL;	
	b包面纸轴绝对运动触发: BOOL;
	b包面纸轴相对运动触发: BOOL;
	b包面纸轴速度模式触发: BOOL;
	b包面纸轴启用限位: BOOL;

//轴状态类	
    b包面纸轴通讯OK: BOOL;
	b包面纸轴使能OK: BOOL; 
	b包面纸轴停止完成: BOOL; 
	b包面纸轴绝对运动完成: BOOL; 
	b包面纸轴相对运动完成: BOOL; 
	b包面纸轴速度模式Busy: BOOL;
	b包面纸轴寸动模式Busy: BOOL;
	b包面纸轴点动模式Busy: BOOL;
	b包面纸轴绝对模式Busy: BOOL;
	b包面纸轴相对模式Busy: BOOL;
	b包面纸轴错误: BOOL;
	b包面纸轴加速中: BOOL;
	b包面纸轴减速中: BOOL;
    b包面纸轴停止中: BOOL;

//数据给定类
	r包面纸轴点动速度给定: LREAL;
	r包面纸轴绝对运动速度给定: LREAL;
	r包面纸轴相对运动速度给定: LREAL;
	r包面纸轴速度模式速度给定: LREAL;
	r包面纸轴寸动速度给定: LREAL;
	
	r包面纸轴绝对运动位置给定: LREAL;		
	r包面纸轴相对运动位置给定: LREAL;
	r包面纸轴寸动位置给定: LREAL;
		
//数据读取类	
    r包面纸轴当前位置: LREAL;
	r包面纸轴当前速度: LREAL;
	r包面纸轴当前扭矩: LREAL;
	
//其它类
    b包面纸轴回零触发: BOOL; 
    b包面纸轴回零Busy: BOOL; 
    b包面纸轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b包面纸轴断使能		AT %MX350.0: BOOL;
	HMI_b包面纸轴单独回原	AT %MX350.1: BOOL;
	HMI_b包面纸轴正向点动	AT %MX350.2: BOOL;
    HMI_b包面纸轴反向点动	AT %MX350.3: BOOL;
	
	HMI_b包面纸轴设为原点	AT %MX350.4: BOOL;
	HMI_b包面纸轴去包面位	AT %MX350.5: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL
	HMI_r包面纸轴当前位置 	AT %MD16100: REAL;
	HMI_r包面纸轴当前速度 	AT %MD16101: REAL;
	HMI_r包面纸轴自动速度 	AT %MD16102: REAL;
	HMI_r包面纸轴手动速度 	AT %MD16103: REAL;
	
	HMI_r包面纸轴导程 		AT %MD16104: REAL;
	HMI_r包面纸轴齿轮比分子 AT %MD16105: REAL;
	HMI_r包面纸轴齿轮比分母 AT %MD16106: REAL;
	
	HMI_r包面纸轴回零快速 	AT %MD16107: REAL;
	HMI_r包面纸轴回零慢速 	AT %MD16108: REAL;
	HMI_r包面纸轴正限位 	AT %MD16109: REAL;
	HMI_r包面纸轴负限位 	AT %MD16110: REAL;
	
	HMI_r包面纸轴加速时间 	AT %MD16111: REAL;
	HMI_r包面纸轴减速时间 	AT %MD16112: REAL;
	
	HMI_r包面纸轴包面位 	AT %MD16113: REAL;
END_VAR



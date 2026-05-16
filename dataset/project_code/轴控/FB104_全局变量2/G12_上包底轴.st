VAR_GLOBAL
	FB_AxisControl_上包底轴: FB_轴控块;

//轴触发类		 
	b上包底轴正向点动: BOOL;
	b上包底轴反向点动: BOOL;
	b上包底轴正向寸动: BOOL;
	b上包底轴反向寸动: BOOL;	
	b上包底轴停止触发: BOOL;
	b上包底轴复位触发: BOOL;	
	b上包底轴绝对运动触发: BOOL;
	b上包底轴相对运动触发: BOOL;
	b上包底轴速度模式触发: BOOL;
	b上包底轴启用限位: BOOL;

//轴状态类	
    b上包底轴通讯OK: BOOL;
	b上包底轴使能OK: BOOL; 
	b上包底轴停止完成: BOOL; 
	b上包底轴绝对运动完成: BOOL; 
	b上包底轴相对运动完成: BOOL; 
	b上包底轴速度模式Busy: BOOL;
	b上包底轴寸动模式Busy: BOOL;
	b上包底轴点动模式Busy: BOOL;
	b上包底轴绝对模式Busy: BOOL;
	b上包底轴相对模式Busy: BOOL;
	b上包底轴错误: BOOL;
	b上包底轴加速中: BOOL;
	b上包底轴减速中: BOOL;
    b上包底轴停止中: BOOL;

//数据给定类
	r上包底轴点动速度给定: LREAL;
	r上包底轴绝对运动速度给定: LREAL;
	r上包底轴相对运动速度给定: LREAL;
	r上包底轴速度模式速度给定: LREAL;
	r上包底轴寸动速度给定: LREAL;
	
	r上包底轴绝对运动位置给定: LREAL;		
	r上包底轴相对运动位置给定: LREAL;
	r上包底轴寸动位置给定: LREAL;
		
//数据读取类	
    r上包底轴当前位置: LREAL;
	r上包底轴当前速度: LREAL;
	r上包底轴当前扭矩: LREAL;
	
//其它类
    b上包底轴回零触发: BOOL; 
    b上包底轴回零Busy: BOOL; 
    b上包底轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b上包底轴断使能		AT %MX355.0: BOOL;
	HMI_b上包底轴单独回原	AT %MX355.1: BOOL;
	HMI_b上包底轴正向点动	AT %MX355.2: BOOL;
    HMI_b上包底轴反向点动	AT %MX355.3: BOOL;
	
	HMI_b上包底轴设为原点	AT %MX355.4: BOOL;
	HMI_b上包底轴去接底板位	AT %MX355.5: BOOL;
	HMI_b上包底轴去送底板位	AT %MX355.6: BOOL;
	HMI_b上包底轴去送等待位	AT %MX355.7: BOOL;
	
	HMI_b上包底轴去送底板A位 AT %MX356.0: BOOL;
	HMI_b上包底轴去送底板B位 AT %MX356.1: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL	
	HMI_r上包底轴当前位置 	AT %MD16150: REAL;
	HMI_r上包底轴当前速度 	AT %MD16151: REAL;
	HMI_r上包底轴自动速度 	AT %MD16152: REAL;
	HMI_r上包底轴手动速度 	AT %MD16153: REAL;
	
	HMI_r上包底轴导程 		AT %MD16154: REAL;
	HMI_r上包底轴齿轮比分子 AT %MD16155: REAL;
	HMI_r上包底轴齿轮比分母 AT %MD16156: REAL;
	
	HMI_r上包底轴回零快速 	AT %MD16157: REAL;
	HMI_r上包底轴回零慢速 	AT %MD16158: REAL;
	HMI_r上包底轴正限位 	AT %MD16159: REAL;
	HMI_r上包底轴负限位 	AT %MD16160: REAL;
	
	HMI_r上包底轴加速时间	AT %MD16161: REAL;
	HMI_r上包底轴减速时间	AT %MD16162: REAL;
	
	HMI_r上包底轴接底板位	AT %MD16163: REAL;
	HMI_r上包底轴送底板位	AT %MD16164: REAL;
	HMI_r上包底轴送等待位	AT %MD16165: REAL;
	
	HMI_r上包底轴送底板A位	AT %MD16166: REAL;
	HMI_r上包底轴送底板B位	AT %MD16167: REAL;
	
END_VAR



VAR_GLOBAL
	FB_AxisControl_横移A轴: FB_轴控块;

//轴触发类		 
	b横移A轴正向点动: BOOL;
	b横移A轴反向点动: BOOL;
	b横移A轴正向寸动: BOOL;
	b横移A轴反向寸动: BOOL;	
	b横移A轴停止触发: BOOL;
	b横移A轴复位触发: BOOL;	
	b横移A轴绝对运动触发: BOOL;
	b横移A轴相对运动触发: BOOL;
	b横移A轴速度模式触发: BOOL;
	b横移A轴启用限位: BOOL;

//轴状态类	
    b横移A轴通讯OK: BOOL;
	b横移A轴使能OK: BOOL; 
	b横移A轴停止完成: BOOL; 
	b横移A轴绝对运动完成: BOOL; 
	b横移A轴相对运动完成: BOOL; 
	b横移A轴速度模式Busy: BOOL;
	b横移A轴寸动模式Busy: BOOL;
	b横移A轴点动模式Busy: BOOL;
	b横移A轴绝对模式Busy: BOOL;
	b横移A轴相对模式Busy: BOOL;
	b横移A轴错误: BOOL;
	b横移A轴加速中: BOOL;
	b横移A轴减速中: BOOL;
    b横移A轴停止中: BOOL;

//数据给定类
	r横移A轴点动速度给定: LREAL;
	r横移A轴绝对运动速度给定: LREAL;
	r横移A轴相对运动速度给定: LREAL;
	r横移A轴速度模式速度给定: LREAL;
	r横移A轴寸动速度给定: LREAL;
	
	r横移A轴绝对运动位置给定: LREAL;		
	r横移A轴相对运动位置给定: LREAL;
	r横移A轴寸动位置给定: LREAL;
		
//数据读取类	
    r横移A轴当前位置: LREAL;
	r横移A轴当前速度: LREAL;
	r横移A轴当前扭矩: LREAL;
	
//其它类
    b横移A轴回零触发: BOOL; 
    b横移A轴回零Busy: BOOL; 
    b横移A轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b横移A轴断使能 	 AT %MX320.0: BOOL;
	HMI_b横移A轴单独回原 AT %MX320.1: BOOL;
	HMI_b横移A轴正向点动 AT %MX320.2: BOOL;
    HMI_b横移A轴反向点动 AT %MX320.3: BOOL;
	
	HMI_b横移A轴设为原点 AT %MX320.4: BOOL;
	HMI_b横移A轴去接底板位 AT %MX320.5: BOOL;
	HMI_b横移A轴去成型位 AT %MX320.6: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL	
	HMI_r横移A轴当前位置 	AT %MD15800: REAL;
	HMI_r横移A轴当前速度 	AT %MD15801: REAL;
	HMI_r横移A轴自动速度 	AT %MD15802: REAL;
	HMI_r横移A轴手动速度 	AT %MD15803: REAL;
	
	HMI_r横移A轴导程 		AT %MD15804: REAL;
	HMI_r横移A轴齿轮比分子 	AT %MD15805: REAL;
	HMI_r横移A轴齿轮比分母 	AT %MD15806: REAL;
	
	HMI_r横移A轴回零快速 	AT %MD15807: REAL;
	HMI_r横移A轴回零慢速 	AT %MD15808: REAL;
	HMI_r横移A轴正限位 		AT %MD15809: REAL;
	HMI_r横移A轴负限位 		AT %MD15810: REAL;
	
	HMI_r横移A轴加速时间 	AT %MD15811: REAL;
	HMI_r横移A轴减速时间 	AT %MD15812: REAL;
	
	HMI_r横移A轴接底板位 	AT %MD15813: REAL;
	HMI_r横移A轴成型位 		AT %MD15814: REAL;

END_VAR



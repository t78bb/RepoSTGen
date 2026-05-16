VAR_GLOBAL
	FB_AxisControl_铲灰板轴: FB_轴控块;

//轴触发类		 
	b铲灰板轴正向点动: BOOL;
	b铲灰板轴反向点动: BOOL;
	b铲灰板轴正向寸动: BOOL;
	b铲灰板轴反向寸动: BOOL;	
	b铲灰板轴停止触发: BOOL;
	b铲灰板轴复位触发: BOOL;	
	b铲灰板轴绝对运动触发: BOOL;
	b铲灰板轴相对运动触发: BOOL;
	b铲灰板轴速度模式触发: BOOL;
	b铲灰板轴启用限位: BOOL;

//轴状态类	
    b铲灰板轴通讯OK: BOOL;
	b铲灰板轴使能OK: BOOL; 
	b铲灰板轴停止完成: BOOL; 
	b铲灰板轴绝对运动完成: BOOL; 
	b铲灰板轴相对运动完成: BOOL; 
	b铲灰板轴速度模式Busy: BOOL;
	b铲灰板轴寸动模式Busy: BOOL;
	b铲灰板轴点动模式Busy: BOOL;
	b铲灰板轴绝对模式Busy: BOOL;
	b铲灰板轴相对模式Busy: BOOL;
	b铲灰板轴错误: BOOL;
	b铲灰板轴加速中: BOOL;
	b铲灰板轴减速中: BOOL;
    b铲灰板轴停止中: BOOL;

//数据给定类
	r铲灰板轴点动速度给定: LREAL;
	r铲灰板轴绝对运动速度给定: LREAL;
	r铲灰板轴相对运动速度给定: LREAL;
	r铲灰板轴速度模式速度给定: LREAL;
	r铲灰板轴寸动速度给定: LREAL;
	
	r铲灰板轴绝对运动位置给定: LREAL;		
	r铲灰板轴相对运动位置给定: LREAL;
	r铲灰板轴寸动位置给定: LREAL;
		
//数据读取类	
    r铲灰板轴当前位置: LREAL;
	r铲灰板轴当前速度: LREAL;
	r铲灰板轴当前扭矩: LREAL;
	
//其它类
    b铲灰板轴回零触发: BOOL; 
    b铲灰板轴回零Busy: BOOL; 
    b铲灰板轴回零完成: BOOL; 
END_VAR


//HMI_PLC_BOOL映射
VAR_GLOBAL	
	HMI_b铲灰板轴断使能		AT %MX345.0: BOOL;
	HMI_b铲灰板轴单独回原	AT %MX345.1: BOOL;
	HMI_b铲灰板轴正向点动	AT %MX345.2: BOOL;
    HMI_b铲灰板轴反向点动	AT %MX345.3: BOOL;
	
	HMI_b铲灰板轴设为原点	AT %MX345.4: BOOL;
	HMI_b铲灰板轴去铲出位	AT %MX345.5: BOOL;
END_VAR

//HMI_PLC_Data映射
VAR_GLOBAL	
	HMI_r铲灰板轴当前位置 	AT %MD16050: REAL;
	HMI_r铲灰板轴当前速度 	AT %MD16051: REAL;
	HMI_r铲灰板轴自动速度 	AT %MD16052: REAL;
	HMI_r铲灰板轴手动速度 	AT %MD16053: REAL;
	
	HMI_r铲灰板轴导程 		AT %MD16054: REAL;
	HMI_r铲灰板轴齿轮比分子 AT %MD16055: REAL;
	HMI_r铲灰板轴齿轮比分母 AT %MD16056: REAL;
	
	HMI_r铲灰板轴回零快速 	AT %MD16057: REAL;
	HMI_r铲灰板轴回零慢速 	AT %MD16058: REAL;
	HMI_r铲灰板轴正限位 	AT %MD16059: REAL;
	HMI_r铲灰板轴负限位 	AT %MD16060: REAL;
	
	HMI_r铲灰板轴加速时间 	AT %MD16061: REAL;
	HMI_r铲灰板轴减速时间 	AT %MD16062: REAL;
	
	HMI_r铲灰板轴铲出位 	AT %MD16063: REAL;

END_VAR



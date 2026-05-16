
VAR_GLOBAL
	HMI_d设备总产量         AT %MD10251: UDINT; 
	HMI_d设备故障码			AT %MD10252: UDINT; 
	HMI_d设备运行天数		AT %MD10253: UDINT; 
	HMI_d产能				AT %MD10254: UDINT;
	
	HMI_d设备运行速度       AT %MD15250: REAL;
	HMI_r推底板延时         AT %MD15251: REAL;
	
	HMI_r盒子长度 			AT %MD15252: REAL;
	HMI_r盒子宽度 			AT %MD15253: REAL;
	HMI_r盒子高度 			AT %MD15254: REAL;
	HMI_r灰板厚度 			AT %MD15255: REAL;
	HMI_r成型间距 			AT %MD15256: REAL;
	HMI_r铲刀原点距离 		AT %MD15257: REAL;
	HMI_r毛刷原点距离 		AT %MD15258: REAL;
END_VAR
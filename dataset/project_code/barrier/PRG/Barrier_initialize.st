//默认自动使能
gUI.mode.autoEnable	:= TRUE;
gUI.mode.usePID := TRUE;

//initialize boundary val
	//ground
	gDev.grd[	1	].sensor.retractVal	:=	4.4	;		gDev.grd[	1	].sensor.extendVal	:=	108 	;
	gDev.grd[	2	].sensor.retractVal	:=	3.5	;		gDev.grd[	2	].sensor.extendVal	:=	113.4	;
	gDev.grd[	3	].sensor.retractVal	:=	4.1	;		gDev.grd[	3	].sensor.extendVal	:=	110 	;
	gDev.grd[	4	].sensor.retractVal	:=	1	;		gDev.grd[	4	].sensor.extendVal	:=	112.3	;		//结构问题暂不动
	gDev.grd[	5	].sensor.retractVal	:=	4.0	;		gDev.grd[	5	].sensor.extendVal	:=	107.1-0.5	;
	gDev.grd[	6	].sensor.retractVal	:=	3.5	;		gDev.grd[	6	].sensor.extendVal	:=	110.5	;
	gDev.grd[	7	].sensor.retractVal	:=	5	;		gDev.grd[	7	].sensor.extendVal	:=	109.7   ;
	gDev.grd[	8	].sensor.retractVal	:=	4.8	;		gDev.grd[	8	].sensor.extendVal	:=	109.2	;
	gDev.grd[	9	].sensor.retractVal	:=	3.2	;		gDev.grd[	9	].sensor.extendVal	:=	108 -0.5 	;
	gDev.grd[	10	].sensor.retractVal	:=	6.9	;		gDev.grd[	10	].sensor.extendVal	:=	112 	;
(*	
	gDev.grd[	7	].sensor.retractVal	:=	3.6	;		gDev.grd[	7	].sensor.extendVal	:=	108.3	;
	gDev.grd[	8	].sensor.retractVal	:=	3.5	;		gDev.grd[	8	].sensor.extendVal	:=	113.1	;
	gDev.grd[	9	].sensor.retractVal	:=	3.2	;		gDev.grd[	9	].sensor.extendVal	:=	107.3	;
	gDev.grd[	10	].sensor.retractVal	:=	3.4	;		gDev.grd[	10	].sensor.extendVal	:=	113.5	;*)

	//sky	
	gDev.sky[	0	].sensor.retractVal	:=	3.7	;		gDev.sky[	0	].sensor.extendVal	:=	213.6	;
	gDev.sky[	1	].sensor.retractVal	:=	8.8	;		gDev.sky[	1	].sensor.extendVal	:=	113.1	;
	gDev.sky[	2	].sensor.retractVal	:=	3.5	;		gDev.sky[	2	].sensor.extendVal	:=	113.0	;
	gDev.sky[	3	].sensor.retractVal	:=	3.5	;		gDev.sky[	3	].sensor.extendVal	:=	111.0	;
	gDev.sky[	4	].sensor.retractVal	:=	1	;		gDev.sky[	4	].sensor.extendVal	:=	58.2	;
	gDev.sky[	5	].sensor.retractVal	:=	3.2	;		gDev.sky[	5	].sensor.extendVal	:=	106.6	;
	gDev.sky[	6	].sensor.retractVal	:=	6.2	;		gDev.sky[	6	].sensor.extendVal	:=	109.8	;
(*	
	gDev.sky[	7	].sensor.retractVal	:=	1	;		gDev.sky[	7	].sensor.extendVal	:=	113.4	;		//default:115
	gDev.sky[	8	].sensor.retractVal	:=	1	;		gDev.sky[	8	].sensor.extendVal	:=	112.2	;
	gDev.sky[	9	].sensor.retractVal	:=	1	;		gDev.sky[	9	].sensor.extendVal	:=	112.3	;
	gDev.sky[	10	].sensor.retractVal	:=	1	;		gDev.sky[	10	].sensor.extendVal	:=	66.3	;
*)
	
	gDev.sky[	7	].sensor.retractVal	:=	5	;		gDev.sky[	7	].sensor.extendVal	:=	108.7	;		//default:115
	gDev.sky[	8	].sensor.retractVal	:=	8.6	;		gDev.sky[	8	].sensor.extendVal	:=	113.3	;
	gDev.sky[	9	].sensor.retractVal	:=	12.9 ;		gDev.sky[	9	].sensor.extendVal	:=	113.8	;
	gDev.sky[	10	].sensor.retractVal	:=	3.9 ;		gDev.sky[	10	].sensor.extendVal	:=	111.5	;

	
//初始化默认伸缩比例量
	gDev.grd[1].ctrl.exPct :=	28		;			gDev.grd[1].ctrl.rtPct :=	25		;
	gDev.grd[2].ctrl.exPct :=	28		;			gDev.grd[2].ctrl.rtPct :=	25		;
	gDev.grd[3].ctrl.exPct :=	30		;			gDev.grd[3].ctrl.rtPct :=	25		;
	gDev.grd[4].ctrl.exPct :=	28		;			gDev.grd[4].ctrl.rtPct :=	25		;
	gDev.grd[5].ctrl.exPct :=	33		;			gDev.grd[5].ctrl.rtPct :=	33		;		//exPct:=26	rtPct:=21 二次比例
	gDev.grd[6].ctrl.exPct :=	28		;			gDev.grd[6].ctrl.rtPct :=	25		;
	gDev.grd[7].ctrl.exPct :=	28		;			gDev.grd[7].ctrl.rtPct :=	25		;
	gDev.grd[8].ctrl.exPct :=	28		;			gDev.grd[8].ctrl.rtPct :=	25		;
	gDev.grd[9].ctrl.exPct :=	28		;			gDev.grd[9].ctrl.rtPct :=	25		;
	gDev.grd[10].ctrl.exPct :=	28		;			gDev.grd[10].ctrl.rtPct :=	25		;
	
	gDev.sky[0].ctrl.exPct :=	35		;			gDev.sky[0].ctrl.rtPct :=	41		;
	gDev.sky[1].ctrl.exPct :=	25		;			gDev.sky[1].ctrl.rtPct :=	28		;
	gDev.sky[2].ctrl.exPct :=	25		;			gDev.sky[2].ctrl.rtPct :=	28		;
	gDev.sky[3].ctrl.exPct :=	25		;			gDev.sky[3].ctrl.rtPct :=	28		;
	gDev.sky[4].ctrl.exPct :=	25		;			gDev.sky[4].ctrl.rtPct :=	28		;
	gDev.sky[5].ctrl.exPct :=	27		;			gDev.sky[5].ctrl.rtPct :=	30.5	;
	gDev.sky[6].ctrl.exPct :=	25		;			gDev.sky[6].ctrl.rtPct :=	29		;
	gDev.sky[7].ctrl.exPct :=	25		;			gDev.sky[7].ctrl.rtPct :=	28		;
	gDev.sky[8].ctrl.exPct :=	25		;			gDev.sky[8].ctrl.rtPct :=	28		;
	gDev.sky[9].ctrl.exPct :=	25		;			gDev.sky[9].ctrl.rtPct :=	28		;
	gDev.sky[10].ctrl.exPct :=	25		;			gDev.sky[10].ctrl.rtPct :=	28		;



//initialize device name

											gUI.sky[	0	].wname	:=	"天轨1#"	;
gUI.grd[	1	].wname	:=	"地轨1#"	;	gUI.sky[	1	].wname	:=	"天轨2#"	;
gUI.grd[	2	].wname	:=	"地轨2#"	;	gUI.sky[	2	].wname	:=	"天轨3#"	;
gUI.grd[	3	].wname	:=	"地轨3#"	;	gUI.sky[	3	].wname	:=	"天轨4#"	;
gUI.grd[	4	].wname	:=	"地轨4#"	;	gUI.sky[	4	].wname	:=	"天轨5#"	;
gUI.grd[	5	].wname	:=	"地轨5#"	;	gUI.sky[	5	].wname	:=	"天轨6#"	;
gUI.grd[	6	].wname	:=	"地轨6#"	;	gUI.sky[	6	].wname	:=	"天轨7#"	;
gUI.grd[	7	].wname	:=	"地轨7#"	;	gUI.sky[	7	].wname	:=	"天轨8#"	;
gUI.grd[	8	].wname	:=	"地轨8#"	;	gUI.sky[	8	].wname	:=	"天轨9#"	;
gUI.grd[	9	].wname	:=	"地轨9#"	;	gUI.sky[	9	].wname	:=	"天轨10#"	;
gUI.grd[	10	].wname	:=	"地轨10#"	;	gUI.sky[	10	].wname	:=	"天轨11#"	;

												gUI.sky[	0	].hzname	:=	"天.起竖"	;
gUI.grd[	1	].hzname	:=	"地.横1"	;	gUI.sky[	1	].hzname	:=	"天.横1"	;
gUI.grd[	2	].hzname	:=	"地.纵1"	;	gUI.sky[	2	].hzname	:=	"天.纵1"	;
gUI.grd[	3	].hzname	:=	"地.横2"	;	gUI.sky[	3	].hzname	:=	"天.横2"	;
gUI.grd[	4	].hzname	:=	"地.横3"	;	gUI.sky[	4	].hzname	:=	"天.横3"	;
gUI.grd[	5	].hzname	:=	"地.横4"	;	gUI.sky[	5	].hzname	:=	"天.横4"	;
gUI.grd[	6	].hzname	:=	"地.横5"	;	gUI.sky[	6	].hzname	:=	"天.横5"	;
gUI.grd[	7	].hzname	:=	"地.纵2"	;	gUI.sky[	7	].hzname	:=	"天.纵2"	;
gUI.grd[	8	].hzname	:=	"地.横6"	;	gUI.sky[	8	].hzname	:=	"天.横6"	;
gUI.grd[	9	].hzname	:=	"地.横7"	;	gUI.sky[	9	].hzname	:=	"天.横7"	;
gUI.grd[	10	].hzname	:=	"地.横8"	;	gUI.sky[	10	].hzname	:=	"天.横8"	;

											gUI.sky[	0	].name	:=	'SKY_00'	;
gUI.grd[	1	].name	:=	'GRD_01'	;	gUI.sky[	1	].name	:=	'SKY_01'	;
gUI.grd[	2	].name	:=	'GRD_02'	;	gUI.sky[	2	].name	:=	'SKY_02'	;
gUI.grd[	3	].name	:=	'GRD_03'	;	gUI.sky[	3	].name	:=	'SKY_03'	;
gUI.grd[	4	].name	:=	'GRD_04'	;	gUI.sky[	4	].name	:=	'SKY_04'	;
gUI.grd[	5	].name	:=	'GRD_05'	;	gUI.sky[	5	].name	:=	'SKY_05'	;
gUI.grd[	6	].name	:=	'GRD_06'	;	gUI.sky[	6	].name	:=	'SKY_06'	;
gUI.grd[	7	].name	:=	'GRD_07'	;	gUI.sky[	7	].name	:=	'SKY_07'	;
gUI.grd[	8	].name	:=	'GRD_08'	;	gUI.sky[	8	].name	:=	'SKY_08'	;
gUI.grd[	9	].name	:=	'GRD_09'	;	gUI.sky[	9	].name	:=	'SKY_09'	;
gUI.grd[	10	].name	:=	'GRD_10'	;	gUI.sky[	10	].name	:=	'SKY_10'	;



//使用传感器当前位置作为初始化目标位移点
//(*
FOR gi := 1 TO 10 DO
	IF gDev.grd[gi].sensor.position <> 0.0 THEN
		gDev.grd[gi].ctrl.pos.Set_Point := gDev.grd[gi].sensor.position;
	ELSE
		gDev.grd[gi].ctrl.isError := TRUE;
	END_IF
END_FOR

FOR si := 0 TO 10 DO
	IF gDev.sky[si].sensor.position <> 0.0 THEN
		gDev.sky[si].ctrl.pos.Set_Point := gDev.sky[si].sensor.position;
	ELSE
		gDev.sky[si].ctrl.isError := TRUE;
	END_IF
END_FOR
//*)
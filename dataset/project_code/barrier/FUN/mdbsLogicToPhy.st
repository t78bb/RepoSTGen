FUNCTION_BLOCK mdbsLogicToPhy	//modbus华中挡板地址编号对应本地索引编号
VAR_INPUT
	section		:INT;	//区域限定 1:skyExt, 2:skyRet, 3:grdExt, 4:grdRet)
	lgcIdx		:INT;	//华中对应的地址	10,14{1..10}  17,20{1..11}
END_VAR
VAR_OUTPUT
	level		:INT;	//1->地轨	2->天轨
	phyIdx		:INT;	//内存物理地址对应数组索引
	direct		:TargetDirect;
END_VAR
VAR
END_VAR

(**
 * 将华中指令解析为要动作挡板的标号
 * (level:1->地轨	2->天轨)(phyIdx:内存物理地址对应数组索引)
 *)
CASE section OF
	1://区域限定1:skyExtend)
		level := 2;
		direct := TargetDirect.extend;
		CASE lgcIdx OF
			1:	phyIdx := 1;		//横1	->	sky1
			2:	phyIdx := 3;		//横2	->	sky3
			3:	phyIdx := 4;		//横3	->	sky4
			4:	phyIdx := 5;		//横4	->	sky5
			5:	phyIdx := 6;		//横5	->	sky6
			6:	phyIdx := 8;		//横6	->	sky8
			7:	phyIdx := 9;		//横7	->	sky9
			8:	phyIdx := 10;		//横8	->	sky10
			9:	phyIdx := 2;		//纵1	->	sky2
			10:	phyIdx := 7;		//纵2	->	sky7
			11:	phyIdx := 0;		//起竖	->	sky0
		END_CASE

	2://区域限定2:skyRetract)
		level := 2;
		direct := TargetDirect.retract;
		CASE lgcIdx OF
			1:	phyIdx := 1;		//横1	->	sky1
			2:	phyIdx := 3;		//横2	->	sky3
			3:	phyIdx := 4;		//横3	->	sky4
			4:	phyIdx := 5;		//横4	->	sky5
			5:	phyIdx := 6;		//横5	->	sky6
			6:	phyIdx := 8;		//横6	->	sky8
			7:	phyIdx := 9;		//横7	->	sky9
			8:	phyIdx := 10;		//横8	->	sky10
			9:	phyIdx := 2;		//纵1	->	sky2
			10:	phyIdx := 7;		//纵2	->	sky7
			11:	phyIdx := 0;		//起竖	->	sky0
		END_CASE

	3://区域限定3:grdExtend)
		level := 1;
		direct := TargetDirect.extend;
		CASE lgcIdx OF
			1:	phyIdx := 1;		//横1	->	grd1
			2:	phyIdx := 3;		//横2	->	grd3
			3:	phyIdx := 4;		//横3	->	grd4
			4:	phyIdx := 5;		//横4	->	grd5
			5:	phyIdx := 6;		//横5	->	grd6
			6:	phyIdx := 8;		//横6	->	grd8
			7:	phyIdx := 9;		//横7	->	grd9
			8:	phyIdx := 10;		//横8	->	grd10
			9:	phyIdx := 2;		//纵1	->	grd2
			10:	phyIdx := 7;		//纵2	->	grd7
		END_CASE
	4://区域限定4:grdRetract)
		level := 1;
		direct := TargetDirect.retract;
		CASE lgcIdx OF
			1:	phyIdx := 1;
			2:	phyIdx := 3;
			3:	phyIdx := 4;
			4:	phyIdx := 5;
			5:	phyIdx := 6;
			6:	phyIdx := 8;
			7:	phyIdx := 9;
			8:	phyIdx := 10;
			9:	phyIdx := 2;
			10:	phyIdx := 7;
		END_CASE
END_CASE
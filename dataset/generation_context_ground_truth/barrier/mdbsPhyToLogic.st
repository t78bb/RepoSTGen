VAR
END_VAR

(**
 * 输入挡板标号，返回华中需要的寄存器地址号
 *)
CASE section OF
	1://区域限定(1:groundExtend)
		CASE phyIdx OF
			1:	lgcIdx := 223;		//grd1e	->	横1	223
			2:	lgcIdx := 231;		//grd2e	->	纵1	231
			3:	lgcIdx := 224;		//grd3e	->	横2	224
			4:	lgcIdx := 225;		//grd4e	->	横3	225
			5:	lgcIdx := 226;		//grd5e	->	横4	226
			6:	lgcIdx := 227;		//grd6e	->	横5	227
			7:	lgcIdx := 232;		//grd7e	->	纵2	232
			8:	lgcIdx := 228;		//grd8e	->	横6	228
			9:	lgcIdx := 229;		//grd9e	->	横7	229
			10:	lgcIdx := 230;		//grd10e->	横8	230
		END_CASE
	2://区域限定(2:groundRetract)
		CASE phyIdx OF
			1:	lgcIdx := 271;		//grd1r	->	横1
			2:	lgcIdx := 279;		//grd2r	->	纵1
			3:	lgcIdx := 272;		//grd3r	->	横2
			4:	lgcIdx := 273;		//grd4r	->	横3
			5:	lgcIdx := 274;		//grd5r	->	横4
			6:	lgcIdx := 275;		//grd6r	->	横5
			7:	lgcIdx := 280;		//grd7r	->	纵2
			8:	lgcIdx := 276;		//grd8r	->	横6
			9:	lgcIdx := 277;		//grd9r	->	横7
			10:	lgcIdx := 278;		//grd10r->	横8
		END_CASE
	3://区域限定(3:skyExtend)
		CASE phyIdx OF
			0:	lgcIdx := 137;		//sky0e	->	起竖	
			1:	lgcIdx := 127;		//sky1e	->	横1	
			2:	lgcIdx := 135;		//sky2e	->	纵1	
			3:	lgcIdx := 128;		//sky3e	->	横2	
			4:	lgcIdx := 129;		//sky4e	->	横3	
			5:	lgcIdx := 130;		//sky5e	->	横4	
			6:	lgcIdx := 131;		//sky6e	->	横5	
			7:	lgcIdx := 136;		//sky7e	->	纵2	
			8:	lgcIdx := 132;		//sky8e	->	横6	
			9:	lgcIdx := 133;		//sky9e	->	横7	
			10:	lgcIdx := 134;		//sky10e->	横8	
		END_CASE
	
	4://区域限定(4:skyRetract)
		CASE phyIdx OF
			0:	lgcIdx := 185;		//sky0r	->	起竖
			1:	lgcIdx := 175;		//sky1r	->	横1
			2:	lgcIdx := 183;		//sky2r	->	纵1
			3:	lgcIdx := 176;		//sky3r	->	横2
			4:	lgcIdx := 177;		//sky4r	->	横3
			5:	lgcIdx := 178;		//sky5r	->	横4
			6:	lgcIdx := 179;		//sky6r	->	横5
			7:	lgcIdx := 184;		//sky7r	->	纵2
			8:	lgcIdx := 180;		//sky8r	->	横6
			9:	lgcIdx := 181;		//sky9r	->	横7
			10:	lgcIdx := 182;		//sky10r->	横8
		END_CASE
END_CASE
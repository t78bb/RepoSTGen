VAR
	
END_VAR

IF devNo > 40000 THEN
	CASE devNo OF
		//地轨
		41010:	level := 1;	idx := 1;
		41020:	level := 1;	idx := 3;
		41030:	level := 1;	idx := 4;
		41040:	level := 1;	idx := 5;
		41050:	level := 1;	idx := 6;
		41060:	level := 1;	idx := 8;
		41070:	level := 1;	idx := 9;
		41080:	level := 1;	idx := 10;
		42010:	level := 1;	idx := 2;
		42020:	level := 1;	idx := 7;
		
		51010:	level := 2;	idx := 1;
		51020:	level := 2;	idx := 3;
		51030:	level := 2;	idx := 4;
		51040:	level := 2;	idx := 5;
		51050:	level := 2;	idx := 6;
		51060:	level := 2;	idx := 8;
		51070:	level := 2;	idx := 9;
		51080:	level := 2;	idx := 10;
		52010:	level := 2;	idx := 2;
		52020:	level := 2;	idx := 7;
		53000:	level := 2;	idx := 0;
		53010:	level := 2;	idx := 0;
	END_CASE
END_IF
PROGRAM FileSaver
VAR
	path 			:STRING:='D:/log';
	intervalMs		:INT := 10;		//间隔时间
	
	init			:BOOL:= TRUE;
	gi				:INT;
	si				:INT;	
	cCtrl			:INT;

	sav				:ARRAY[1..2, 0..10] OF fileSave;
	speed			:INT;
	nowCmd			:ARRAY[1..2, 0..10] OF BOOL;
	canWrite		:ARRAY[1..2, 0..10] OF BOOL;
	nowPosition		:ARRAY[1..2, 0..10] OF INT;
	lastPosition	:ARRAY[1..2, 0..10] OF INT;
	state			:ARRAY[1..2, 0..10] OF INT;
	flag			:ARRAY[1..2, 0..10] OF INT;
END_VAR
VAR CONSTANT
	aOil	:ARRAY [1..7] OF INT :=[9,11,8,8,8,8,23];		
END_VAR

//initialize
IF init THEN
	init := FALSE;
	FOR gi := 1 TO 10 DO
		 sav[1, gi](filePath := path, intervalt := intervalMs);
		 sav[1, gi].createDir(gUI.grd[gi].name);
		 init := FALSE;
	END_FOR
	FOR si := 0 TO 10 DO
		 sav[2, si](filePath := path, intervalt := intervalMs);
		 sav[2, si].createDir(gUI.sky[si].name);
		 init := FALSE;
	END_FOR
END_IF

//detect and record ground and sky
FOR gi := 1 TO 10 DO
	 nowCmd[1, gi] := gUI.grd[gi].btnExtend OR gUI.grd[gi].btnRetract;
	 IF nowCmd[1, gi] THEN
		 IF flag[1, gi] = 0 THEN
			 sav[1, gi].new(devName := gUI.grd[gi].name);
			 flag[1, gi] := 1;
		 END_IF
		 //prepare data
		 getGrdData();
		 //write
		 sav[1, gi].write(positionInt := nowPosition[1, gi],speedInt := speed,
			 				 stateInt := state[1, gi]);
	 ELSE
		 IF flag[1, gi] = 1 THEN
			 sav[1, gi].write(positionInt := nowPosition[1, gi],speedInt := speed,
				 				 stateInt := state[1, gi]);
			 sav[1, gi].close();
			 flag[1, gi] := 0;
		 END_IF
	 END_IF
END_FOR


FOR si := 0 TO 10 DO
	 nowCmd[2, si] := gUI.sky[si].btnExtend OR gUI.sky[si].btnRetract;
	 IF nowCmd[2, si] THEN
		 IF flag[2, si] = 0 THEN
			 sav[2, si].new(devName := gUI.sky[si].name);
			 flag[2, si] := 1;
		 END_IF
		 //prepare data
		 getSkyData();
		 //write
		 sav[2, si].write(positionInt := nowPosition[2, si],speedInt := speed,
			 				 stateInt := state[2, si]);
	 ELSE
		 IF flag[2, si] = 1 THEN
			 sav[2, si].write(positionInt := nowPosition[2, si],speedInt := speed,
				 				 stateInt := state[2, si]);
			 sav[2, si].close();
			 flag[2, si] := 0;
		 END_IF
	 END_IF
END_FOR

TYPE DUT_CAMTABLE :
STRUCT
	//0:X 1:Y  点列表
	Table: ARRAY[0..9] OF ARRAY[0..1] OF REAL;
	
	//0,1:无比例缩放
    fEditorMasterMin: REAL := 0;
    fEditorMasterMax: REAL := 1;
    fEditorSlaveMin: REAL := 0;
    fEditorSlaveMax: REAL := 1;
    fTableMasterMin: REAL := 0;
    fTableMasterMax: REAL := 1;
    fTableSlaveMin: REAL := 0;
    fTableSlaveMax: REAL := 1;
END_STRUCT
END_TYPE

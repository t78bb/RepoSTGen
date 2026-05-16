(*EthercatBUS Cheak*)
IF b调模A轴通讯OK AND b调模B轴通讯OK AND b送面料轴通讯OK AND b取面料轴通讯OK AND b横移A轴通讯OK AND b升降A轴通讯OK AND
    b横移B轴通讯OK AND b升降B轴通讯OK AND b出盒轴通讯OK AND b铲灰板轴通讯OK AND b包面纸轴通讯OK AND b上包底轴通讯OK AND b折边轴通讯OK THEN
	b所有伺服总线通讯OK:=TRUE;
	ELSE
	b所有伺服总线通讯OK:=FALSE;	
END_IF

IF b调模A轴使能OK AND b调模B轴使能OK AND b送面料轴使能OK AND b取面料轴使能OK AND b横移A轴使能OK AND b升降A轴使能OK AND
    b横移B轴使能OK AND b升降B轴使能OK AND b出盒轴使能OK AND b铲灰板轴使能OK AND b包面纸轴使能OK AND b上包底轴使能OK AND b折边轴使能OK THEN
	b所有伺服使能OK:=TRUE;
	ELSE
	b所有伺服使能OK:=FALSE;	
END_IF

IF b调模A轴回零完成 AND b调模B轴回零完成 AND b送面料轴回零完成 AND b取面料轴回零完成 AND b横移A轴回零完成 AND b升降A轴回零完成 AND
    b横移B轴回零完成 AND b升降B轴回零完成 AND b出盒轴回零完成 AND b铲灰板轴回零完成 AND b包面纸轴回零完成 AND b上包底轴回零完成 AND b折边轴回零完成 THEN
	b所有伺服回零OK:=TRUE;
	ELSE
	b所有伺服回零OK:=FALSE;	
END_IF

IF b调模A轴停止中 AND b调模B轴停止中 AND b送面料轴停止中 AND b取面料轴停止中 AND b横移A轴停止中 AND b升降A轴停止中 AND
    b横移B轴停止中 AND b升降B轴停止中 AND b出盒轴停止中 AND b铲灰板轴停止中 AND b包面纸轴停止中 AND b上包底轴停止中 AND b折边轴停止中 THEN
	b所有伺服静止中:=TRUE;
	ELSE
	b所有伺服静止中:=FALSE;	
END_IF
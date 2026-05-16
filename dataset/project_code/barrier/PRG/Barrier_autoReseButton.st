
//更新Button
FOR gi := 1 TO 10 DO
	setButtonByDirect(1, gi, gDev.grd[gi].vector);
END_FOR


FOR si := 0 TO 10 DO
	setButtonByDirect(2, si, gDev.sky[si].vector);
END_FOR

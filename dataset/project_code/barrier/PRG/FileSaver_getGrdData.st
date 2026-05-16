//进制转换 到0.01mm
lastPosition[1, gi] := nowPosition[1, gi];
nowPosition[1, gi] := REAL_TO_INT(10 * gDev.grd[gi].sensor.position);

speed := REAL_TO_INT(gDev.grd[gi].sensor.speed);


state[1, gi] := gDev.grd[gi].state;
//进制转换 到0.01mm
lastPosition[2, si] := nowPosition[2, si];
nowPosition[2, si] := REAL_TO_INT(10 * gDev.sky[si].sensor.position);

speed := REAL_TO_INT(gDev.sky[si].sensor.speed);


state[2, si] := gDev.sky[si].state;
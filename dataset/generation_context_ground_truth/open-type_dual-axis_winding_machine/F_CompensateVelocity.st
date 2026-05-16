
// 检查轴是否在运动（位置是否变化）
IF lOldPos > lNewPos THEN
	IF bUnwinding THEN
		// 放卷：半径减小，速度需要增加
		// 公式：V_new = V_old + V_old * Tk / (R - Tk)
		IF (lRadius - lTk) > 0.01 THEN  // 避免除零
			F_CompensateVelocity := lCurrentVel + lCurrentVel * lTk / (lRadius - lTk);
		ELSE
			F_CompensateVelocity := lCurrentVel;
		END_IF
	ELSE
		// 收卷：半径增加，速度需要降低
		// 公式：V_new = V_old - V_old * Tk / (R + Tk)
		F_CompensateVelocity := lCurrentVel - lCurrentVel * lTk / (lRadius + lTk);
	END_IF
ELSE
	// 位置未变化，保持当前速度
	F_CompensateVelocity := lCurrentVel;
END_IF


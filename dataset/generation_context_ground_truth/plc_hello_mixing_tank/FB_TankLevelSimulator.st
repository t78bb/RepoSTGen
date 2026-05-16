
// 复位逻辑
IF bReset THEN
	rCurrentLevel := rInitialLevel;
END_IF

// 液位计算
// 如果任一填充阀打开则填充，如果排空阀打开则排空
rCurrentLevel := rCurrentLevel
				+ rFillRate1 * BOOL_TO_REAL(bMedium1Opened)
				+ rFillRate2 * BOOL_TO_REAL(bMedium2Opened)
				- rDrainRate * BOOL_TO_REAL(bDrainOpened);

// 限制液位范围 (0-100%)
rCurrentLevel := LIMIT(rMinLevel, rCurrentLevel, rMaxLevel);


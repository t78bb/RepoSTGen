
// 液位开关模拟
bLevelFull := rTankLevel >= rFullThreshold;		// 液位 >= 85% 时，满开关激活
bLevelEmpty := rTankLevel <= rEmptyThreshold;	// 液位 <= 5% 时，空开关激活

F_UpdateLimitSwitches := TRUE;


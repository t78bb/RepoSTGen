
// 半径计算公式：
// R = |√(D²+(Hnew+offset)²) - √(D²+(Hold+offset)²)| / π + Tk
F_CalculateRadius := ABS(SQRT(EXPT(lD,2)+EXPT(lHnew+lOffset,2)) - SQRT(EXPT(lD,2)+EXPT(lHold+lOffset,2))) / SMC_PI + lTk;


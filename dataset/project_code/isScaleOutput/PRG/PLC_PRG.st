PROGRAM PLC_PRG
VAR
    rSensorOutValue : REAL;
    iScaleOutput : INT;
END_VAR

iScaleOutput := F_iScaleOutput(
    rOutput := rSensorOutValue,
    rPhyMin := 4,
    rPhyMax := 20,
    eTerminal := eTerminal_4mA_20mA
);
VAR
    i : UDINT;
    fTmp : SM3M.SMC_Frame;
    afCur : ARRAY[0..1] OF SM3M.SMC_Frame;
END_VAR

i := TO_UDINT(vJoints.n);
afCur[i AND 1] := fTCP_init;
WHILE i > 0 DO
    SMC_Frame_FromScrewAxisAngle(fTmp, aS[i-1], vJoints.a[i-1]);
    SM3M.SMC_Frame_Mult(afCur[(i-1) AND 1], fTmp, afCur[i AND 1]);
    
    i := i - 1;
END_WHILE

fTCP := afCur[0];
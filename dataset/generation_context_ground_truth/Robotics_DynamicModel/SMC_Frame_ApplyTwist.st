VAR
    vTmp : SM3M.SMC_VECTOR3D;
END_VAR

SM3M.SMC_Matrix3_Apply(V_a.w, T_ab.mR, V_b.w);
SM3M.SMC_Matrix3_Apply(V_a.v, T_ab.mR, V_b.v);
SM3M.SMC_V3_Cross(vTmp, T_ab.vT, V_a.w);
SM3M.SMC_V3_Add(V_a.v, V_a.v, vTmp);
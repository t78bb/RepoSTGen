VAR
    v0 : SM3M.SMC_VECTOR3D;
    v1 : SM3M.SMC_VECTOR3D;
END_VAR

SM3M.SMC_V3_Cross(v0, V_lhs.v, V_rhs.w);
SM3M.SMC_V3_Cross(v1, V_lhs.w, V_rhs.v);
SM3M.SMC_V3_Cross(V_dst.w, V_lhs.w, V_rhs.w);
SM3M.SMC_V3_Add(V_dst.v, v0, v1);
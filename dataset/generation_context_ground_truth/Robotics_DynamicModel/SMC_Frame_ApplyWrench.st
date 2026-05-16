VAR
    mR_ : SM3M.SMC_Matrix3;
    wTmp0 : SM3M.SMC_VECTOR3D;
    wTmp1 : SM3M.SMC_VECTOR3D;
END_VAR

/// Applies a coordinate transformation T_ab to a wrench vector F_a in se(3).
///       |mR^T  mR^T*[vT]^T|
/// F_b = |                 | F_a
///       | 0         mR^T  |
FUNCTION SMC_Frame_ApplyWrench
VAR_IN_OUT
    /// Wrench vector in b frame coordinates.
	F_b : WrenchVec;
END_VAR
VAR_IN_OUT CONSTANT
    /// Orientation and position of the b frame
    /// in a frame coordinates.
	T_ab : SM3M.SMC_Frame;
    /// Wrench vector in a frame coordinates.
	F_a : WrenchVec;
END_VAR
VAR
    mR_ : SM3M.SMC_Matrix3;
    wTmp0 : SM3M.SMC_VECTOR3D;
    wTmp1 : SM3M.SMC_VECTOR3D;
END_VAR
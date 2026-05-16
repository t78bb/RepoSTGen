VAR
    T : ARRAY[0..SM3M.SMC_MAX_VEC_DIM] OF SM3M.SMC_Frame;
    V : ARRAY[0..SM3M.SMC_MAX_VEC_DIM] OF TwistVec;
    V_t : ARRAY[0..SM3M.SMC_MAX_VEC_DIM] OF TwistVec;
    F : ARRAY[0..SM3M.SMC_MAX_VEC_DIM] OF WrenchVec;
    
    T_uq : SM3M.SMC_Frame;
    V_uq_s : TwistVec;
    V_t_uq_ss : TwistVec;
    V_prev : TwistVec;
    V_t_prev : TwistVec;
    V_t_brack : TwistVec;
    F_prev : WrenchVec;
    F_V : WrenchVec;
    F_V_t : WrenchVec;
    F_brack : WrenchVec;
    i : DINT;
    
    T_load_inv_Flange : SM3M.SMC_Frame;
    T_load_inv : SM3M.SMC_Frame;
    V_load : TwistVec;
    V_t_load : TwistVec;
    F_load : WrenchVec;
    F_V_load : WrenchVec;
    F_V_t_load : WrenchVec;
    F_brack_load : WrenchVec;
    m_aM_inv : ARRAY[0..SM3M.SMC_MAX_VEC_DIM] OF SM3M.SMC_Frame;
    /// The screw axes of all joints, expressed in the link's frame.
    m_aA : ARRAY[0..SM3M.SMC_MAX_VEC_DIM-1] OF TwistVec;
END_VAR
VAR CONSTANT
/// Degrees of freedom.
	DOF : DINT := 3;
	/// All length values in [m]
	armOneLength : LREAL := 0.4;
	armTwoLength : LREAL := 0.3;
	baseHeight : LREAL := 0.6;
	armOneHeight : LREAL := 0.06;
	armTwoHeight : LREAL := 0.06;
	zAxisLength : LREAL := 0.3;
	zAxisOffset : LREAL := -0.05;
	/// All mass values in [kg]
	armOneMass : LREAL := 3;
	armTwoMass : LREAL := 4;
	zAxisMass : LREAL := 1;
	
	/// The home position of all link frames. |aM[i]| contains
    /// the frame of the ith link expressed in the coordinates of the
    /// (i-1)th link frame.
    /// All frames are expected to be situated at the link's center
    /// of mass.
    m_aM : ARRAY[0..SMRB.MAX_VEC_DIM] OF SM3M.SMC_Frame := [
        /// All values of vT in [m]
        ///
        /// The center of mass of arm 1 expressed in the base coordinate system 0:
        (mR:= (
            aElems:= [
                1, 0, 0,
                0, -1, 0,
                0, 0, -1]),
         vT:= (dX:= armOneLength / 2.0, dY:= 0, dZ:= baseHeight + armOneHeight / 2.0)),
        /// The center of mass of arm 2 expressed in the coordinate system of arm 1:
        (mR:= (
            aElems:= [
                1, 0, 0,
                0, 1, 0,
                0, 0, 1]),
         vT:= (dX:= armOneLength / 2.0 + armTwoLength / 2.0, dY:= 0, dZ:= armOneHeight / 2.0 + armTwoHeight / 2.0)),
        /// The center of mass of the z-axis expressed in the coordinate system of arm 2:
        (mR:= (
            aElems:= [
                1, 0, 0,
                0, 1, 0,
                0, 0, 1]),
         vT:= (dX:= armTwoLength / 2.0, dY:= 0, dZ:= zAxisLength / 2.0 - armTwoHeight / 2.0 + zAxisOffset)),
        /// One additional array entry, to handle an arbitrary load at the TCP, expressed
		/// in the coordinate system of the z-axis.
        (mR:= (
            aElems:= [
                1, 0, 0,
                0, 1, 0,
                0, 0, 1]),
         vT:= (dX:= 0, dY:= 0, dZ:= - zAxisLength / 2.0))];

	/// The spatial inertia matrices of all links, expressed in the
    /// respectives link's frame.
    m_aG : ARRAY[0..SMRB.MAX_VEC_DIM-1] OF SMDYN.DynSpatialInertia := [
        /// All inertia values in [kg m²]
        /// and all mass values in [kg]
        /// Arm 1
        (I:= (
            aElems:= [
                0, 0, 0,
                0, 1/12.0 * armOneMass * armOneLength * armOneLength, 0,
                0, 0, 1/12.0 * armOneMass * armOneLength * armOneLength]),
         m:= armOneMass),
        /// Arm 2
        (I:= (
            aElems:= [
                0, 0, 0,
                0, 1/12.0 * armTwoMass * armTwoLength * armTwoLength, 0,
                0, 0, 1/12.0 * armTwoMass * armTwoLength * armTwoLength]),
         m:= armTwoMass),
        /// z-axis
        (I:= (
            aElems:= [
                1/12.0 * zAxisMass * zAxisLength * zAxisLength, 0, 0,
                0, 1/12.0 * zAxisMass * zAxisLength * zAxisLength, 0,
                0, 0, 0]),
         m:= zAxisMass)];

	/// The screw axes of all joints, expressed in the base frame.
    m_aS : ARRAY[0..SMRB.MAX_VEC_DIM-1] OF TwistVec := [
		/// Angular velocities in [rad/s] and linear velocities in [m/s].
        /// Screw axis of arm 1
        (w:= (dX:= 0, dY:= 0, dZ:= 1),
         v:= (dX:= 0, dY:= 0, dZ:= 0)),
        /// Screw axis of arm 2
        (w:= (dX:= 0, dY:= 0, dZ:= 1),
         v:= (dX:= 0, dY:= -armOneLength, dZ:= 0)),
        /// Screw axis of the z-axis
        (w:= (dX:= 0, dY:= 0, dZ:= 0),
         v:= (dX:= 0, dY:= 0, dZ:= 1))];
END_VAR


SM3M.SMC_V3_Mult(V_t[0].v, g, -1);

T[DOF] := m_aM_inv[DOF];

i := 0;
WHILE i < DOF DO
    SMC_Frame_FromScrewAxisAngle(T_uq, m_aA[i], -uv.v.a[i]);
    SM3M.SMC_Frame_Mult(T[i], T_uq, m_aM_inv[i]);
    
    SMC_Frame_ApplyTwist(V_prev, T[i], V[i]);
    TwistVec_Scale(V_uq_s, m_aA[i], uv.v_s.a[i]);
    TwistVec_Add(V[i+1], V_prev, V_uq_s);
    
    SMC_Frame_ApplyTwist(V_t_prev, T[i], V_t[i]);
    Twist_Bracket_Twist(V_t_brack, V[i+1], m_aA[i]);
    TwistVec_Scale(V_t_brack, V_t_brack, uv.v_s.a[i]);
    TwistVec_Scale(V_t_uq_ss, m_aA[i], uv.v_ss.a[i]);
    TwistVec_Add(V_t[i+1], V_t_prev, V_t_brack);
    TwistVec_Add(V_t[i+1], V_t[i+1], V_t_uq_ss);
    
    i := i + 1;
END_WHILE

SM3M.SMC_Frame_Inverse(T_load_inv_Flange, load.CenterOfMassFrame);
SM3M.SMC_Frame_Mult(T_load_inv, T_load_inv_Flange, T[i]);

SMC_Frame_ApplyTwist(V_load, T_load_inv, V[i]);
SMC_Frame_ApplyTwist(V_t_load, T_load_inv, V_t[i]);
MatSI_ApplyTwist(F_V_t_load, load.Inertia, V_t_load);
MatSI_ApplyTwist(F_V_load, load.Inertia, V_load);
Twist_Bracket_Wrench(F_brack_load, V_load, F_V_load);

WrenchVec_Sub(F_load, F_V_t_load, F_brack_load);
SMC_Frame_ApplyWrench(F[DOF], T_load_inv_Flange, F_load);

WHILE i > 0 DO
    SMC_Frame_ApplyWrench(F_prev, T[i], F[i]);
    MatSI_ApplyTwist(F_V_t, m_aG[i-1], V_t[i]);
    MatSI_ApplyTwist(F_V, m_aG[i-1], V[i]);
    Twist_Bracket_Wrench(F_brack, V[i], F_V);
    
    WrenchVec_Add(F[i-1], F_prev, F_V_t);
    WrenchVec_Sub(F[i-1], F[i-1], F_brack);
    
    torque.a[i-1] := Wrench_Dot_Twist(F[i-1], m_aA[i-1]);
    
    i := i - 1;
END_WHILE

torque.n := DOF;
VAR
	m_dynModel : DynModel_Scara2_Z;
END_VAR
VAR CONSTANT
	/// Frame of the initial robot position.
	ZERO_TCP_FRAME : SM3M.SMC_Frame := (
        mR:= (
            aElems:= [
                1, 0, 0,
                0, 1, 0,
                0, 0, 1]),
        vT:= (
			dX:= m_dynModel.armOneLength + m_dynModel.armTwoLength,
			dY:= 0,
			dZ:= - m_dynModel.baseHeight - m_dynModel.armOneHeight - m_dynModel.zAxisOffset));
END_VAR
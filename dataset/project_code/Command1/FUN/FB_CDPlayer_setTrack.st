METHOD PUBLIC SetTrack : BOOL
VAR_INPUT
	byNewTrack			: UINT;
END_VAR
VAR_OUTPUT
	bPlayerActive		: BOOL;
	byVolume			: BYTE;
	byTrack				: UINT;
END_VAR


byTrack := byNewTrack;
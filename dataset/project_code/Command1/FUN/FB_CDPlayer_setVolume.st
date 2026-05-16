METHOD PUBLIC SetVolume : BOOL
VAR_INPUT
	byNewVolume 		: BYTE;
END_VAR
VAR_OUTPUT
	bPlayerActive		: BOOL;
	byVolume			: BYTE;
	byTrack				: UINT;
END_VAR

byVolume := byNewVolume;
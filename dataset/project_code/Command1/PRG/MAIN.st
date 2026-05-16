PROGRAM MAIN
VAR
	// Invoker
	fbSwitchPanel				: FB_SwitchPanel;
	
	// Receiver
	fbSocket					: FB_Socket;
	refSocket					: REFERENCE TO FB_Socket := fbSocket;	
	fbLamp						: FB_Lamp;
	refLamp						: REFERENCE TO FB_Lamp := fbLamp;	
	fbAirConditioning			: FB_AirConditioning;
	refAirConditioning			: REFERENCE TO FB_AirConditioning := fbAirConditioning;
	fbCDPlayer					: FB_CDPlayer;
	refCDPlayer					: REFERENCE TO FB_CDPlayer := fbCDPlayer;

	// Commands
	fbSocketOnCommand			: FB_SocketOnCommand(refSocket);
	fbSocketOffCommand			: FB_SocketOffCommand(refSocket);
	fbLampSetLevel100Command	: FB_LampSetLevelCommand(refLamp, 100);
	fbLampSetLevel0Command		: FB_LampSetLevelCommand(refLamp, 0);
	fbAirConComfortCommand		: FB_AirConComfortCommand(refAirConditioning);
	fbAirConStandbyCommand		: FB_AirConStandbyCommand(refAirConditioning);	
	fbMusicPlayCommand			: FB_MusicPlayCommand(refCDPlayer);
	fbMusicStopCommand			: FB_MusicStopCommand(refCDPlayer);
	
	bInit						: BOOL := TRUE;
END_VAR

IF (bInit) THEN
	fbSwitchPanel.SetCommand(1, fbSocketOnCommand);
	fbSwitchPanel.SetCommand(2, fbSocketOffCommand);
	fbSwitchPanel.SetCommand(3, fbLampSetLevel100Command);
	fbSwitchPanel.SetCommand(4, fbLampSetLevel0Command);
	fbSwitchPanel.SetCommand(5, fbAirConComfortCommand);
	fbSwitchPanel.SetCommand(6, fbAirConStandbyCommand);
	fbSwitchPanel.SetCommand(7, fbMusicPlayCommand);
	fbSwitchPanel.SetCommand(8, fbMusicStopCommand);
	bInit := FALSE;
ELSE
	fbSwitchPanel();	
END_IF
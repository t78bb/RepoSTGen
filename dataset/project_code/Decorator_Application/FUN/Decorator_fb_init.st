//Constructor of the decorator class called at instanciation
METHOD fb_init
VAR_INPUT
	//Needed values to instanciation
	bInitRetains : BOOL; // TRUE: the Retain-variables are initialized (reset warm / reset cold)
	bInCopyCode : BOOL;  // TRUE  the instance will be copied to the copy-code afterward (online change)
	
	//Reference to the component to be decorated passed as input
	tempInputComponent : Component_Interface;
END_VAR

//This constructor stores the component to be decorated in its field tempComponent in orer to be used by all its subclasses
THIS^.tempComponent := tempInputComponent;

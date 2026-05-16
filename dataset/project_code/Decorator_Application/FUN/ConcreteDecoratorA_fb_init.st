//Constructor of the decorating class called at instanciation
METHOD fb_init
VAR_INPUT
	//Needed values to instanciation
	bInitRetains : BOOL; // TRUE: the Retain-variables are initialized (reset warm / reset cold)
	bInCopyCode : BOOL;  // TRUE  the instance will be copied to the copy-code afterward (online change)
	
	//Reference to the component to be decorated passed as input
	tempInputComponent : Component_Interface;
END_VAR

//Calls the constructor (fb_init) in its SUPER class (Decorator)
// in order to pass the component to be decorated to the Decorator constructor.
SUPER^.fb_init(TRUE, TRUE, tempInputComponent);
//Sets the default description for the objects of this class
THIS^.sDescription := ' Decorator A';
//Sets the default value for the objects of this class
THIS^.rValue := 0.5;
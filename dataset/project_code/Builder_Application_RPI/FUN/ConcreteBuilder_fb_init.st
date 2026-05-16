//This is the concrete builder class, reponsible for building the final product objecMETHOD fb_init
VAR_INPUT
	//Necesary fields for the constructor
	bInitRetains : BOOL; // TRUE: the Retain-variables are initialized (reset warm / reset cold)
	bInCopyCode : BOOL;  // TRUE  the instance will be copied to the copy-code afterward (online change)	

	//The constructor receives the specifications for this ConcreteBuilder instance 
	//Just in case the concrete builder could change the specifications in the future, otherwise
	// this specifications should be constant.
	specs : ARRAY [1..4] OF STRING;
END_VAR
VAR
	//Holds an internal reference to how the final product shoud be so the builder class can build it on the fly 
	// without any help from other classes exepting the Director class that is going to be passing the special
	//specifications to the builder.
	localProduct : Product;
	
	//Stores the specifications, sent by the client, of the final product to be built.
	specifications : ARRAY [1..4] OF STRING;
END_VAR


//Stores the specifications on its own specifications field.
THIS^.specifications := specs;

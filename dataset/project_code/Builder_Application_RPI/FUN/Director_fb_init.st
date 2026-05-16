//This constructor is called at instanciation it is necessary to instanciate the Director instance.
//The specifications of the concreteBuilder instance stored in the Director instance should be set first by the client
// otherwise a Data Recursion error is caused
METHOD fb_init
VAR_INPUT
	//Reference to the builder that is going to be building the final product object.
	inputConcreteBuilder : ConcreteBuilder(specs := inputConcreteBuilder.specifications);
	//Necesary fields for the constructor
	bInitRetains : BOOL; // TRUE: the Retain-variables are initialized (reset warm / reset cold)
	bInCopyCode : BOOL;  // TRUE  the instance will be copied to the copy-code afterward (online change)
	
	//Reference a concreteBuilder instance to instanciate the Director.
	inputConcreteBuilder : ConcreteBuilder(specs := defaultArray) ;	
END_VAR
VAR_OUTPUT
END_VAR
VAR
	//Holds a reference to the concrete builder object to send the specifications of the final product to it.
	concreteBuilder : ConcreteBuilder(specs := THIS^.concreteBuilder.specifications);
		//Variable to isntanciate the concreteBuilder instance on the input section. It does not affect the Directors instanciation.
	defaultArray : ARRAY [1..4] OF STRING := ['Default' ,'Default' ,'Default' ,'Default'];
END_VAR


//Creates the concreteBuilder instance that will be building the final product object in its own field THIS^.concreteBuilder
//This instance is empty because we can not use Data Recursion with the inputConcreteInstance instanciation.
//So this concreteBuilder instance should be changed by the client before a Construct() request is called on the Director for the first time only.
THIS^.concreteBuilder := inputConcreteBuilder;
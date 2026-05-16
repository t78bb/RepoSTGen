{attribute 'enable_dynamic_creation'}
//The director class is responsible to delegate the construction of the final product object 
// to a concrete builder object.
FUNCTION_BLOCK Director
VAR_INPUT
	//Reference to the builder that is going to be building the final product object.
	inputConcreteBuilder : ConcreteBuilder(specs := inputConcreteBuilder.specifications);
END_VAR
VAR_OUTPUT
END_VAR
VAR
	//Holds a reference to the concrete builder object to send the specifications of the final product to it.
	concreteBuilder : ConcreteBuilder(specs := THIS^.concreteBuilder.specifications);
END_VAR

//Stores the reference to which builder will be building the final product object in its own field THIS^.concreteBuilder
THIS^.concreteBuilder := inputConcreteBuilder;
VAR
	//Holds a reference to the concrete builder object to send the specifications of the final product to it.
	concreteBuilder : ConcreteBuilder(specs := THIS^.concreteBuilder.specifications);
END_VAR

//Stores the reference to which builder will be building the final product object in its own field THIS^.concreteBuilder
THIS^.concreteBuilder := inputConcreteBuilder;
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
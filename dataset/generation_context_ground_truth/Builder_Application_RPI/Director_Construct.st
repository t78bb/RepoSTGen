VAR
	//Holds a reference to the concrete builder object to send the specifications of the final product to it.
	concreteBuilder : ConcreteBuilder(specs := THIS^.concreteBuilder.specifications);
END_VAR

//The Director tells its concreteBuilder instance to build the final product step by step passing the specifications stored in the 
// concreteBuilder array THIS^.specifications[1..4]

//Step 1 "Main Part"
THIS^.concreteBuilder.Set_Main_Part(THIS^.concreteBuilder.specifications[1]);
//Step 2 "Part 1"
THIS^.concreteBuilder.Set_Part1(THIS^.concreteBuilder.specifications[2]);
//Step 3 "Part 2"
THIS^.concreteBuilder.Set_Part2(THIS^.concreteBuilder.specifications[3]);
//Step 4 "Part 3"
THIS^.concreteBuilder.Set_Part3(THIS^.concreteBuilder.specifications[4]);

//Finally the concreteBuilder instance in the Director object delivers the final result as a Product object
Construct := THIS^.concreteBuilder.Get_Result();
//Illustrative method of the pattern to set the part1
METHOD Set_Part1
VAR_INPUT
	//Illustrative value (object because it is a TRING) to be set as a product part
	part1	: STRING;
END_VAR
VAR_OUTPUT
END_VAR
VAR
	//Holds an internal reference to how the final product shoud be so the builder class can build it on the fly 
	// without any help from other classes exepting the Director class that is going to be passing the special
	//specifications to the builder.
	localProduct : Product;
	
	//Stores the specifications, sent by the client, of the final product to be built.
	specifications : ARRAY [1..4] OF STRING;
END_VAR
//Sets the passed value to its corresponding field. 
//We can say that the the final product is in process of being built.
//So this is a step into building the final product done by the builder.
THIS^.localProduct.part1 := part1;
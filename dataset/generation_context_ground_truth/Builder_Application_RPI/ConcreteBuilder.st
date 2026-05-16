VAR
	//Holds an internal reference to how the final product shoud be so the builder class can build it on the fly 
	// without any help from other classes exepting the Director class that is going to be passing the special
	//specifications to the builder.
	localProduct : Product;
	
	//Stores the specifications, sent by the client, of the final product to be built.
	specifications : ARRAY [1..4] OF STRING;
END_VAR

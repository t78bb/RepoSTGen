PROGRAM PLC_PRG
VAR
	//Pain Component instance. Object to be decorated.
	basicComponent : ConcreteComponent;
	//Temporal INT value for the PLC to acknowledge if the request has already been handled or not
	iTempDisplay : INT := 0;
	//Real variable to be used in the visualization element as the program's response
	rDisplayValue : REAL;
	//String variable to be used in the visualization element as the program's response
	sDisplayDescription : STRING;
	
	//Pointers to Concrete decorators class to create the needed decorators on demand
	ptrDecorA : POINTER TO ConcreteDecoratorA;
	ptrDecorB : POINTER TO ConcreteDecoratorB;
	ptrDecorC : POINTER TO ConcreteDecoratorC;
	
	//Boolean values for the PLC to process the client's request
	bDecorA : BOOL := FALSE;
	bDecorB : BOOL := FALSE;
	bDecorC : BOOL := FALSE;
	
END_VAR

//The visualization element will handle the request from the client in real time.
//The client can chose any possible combination for the element and the display will show the specific results.

//As there are 3 possible options, the programs checks a 3X3 matrix and checks the last handled request

//If the user has not chosen any Decoration AND iTempDisplay is different to the initial state of 1,
IF NOT bDecorA AND NOT bDecorB AND NOT bDecorC AND iTempDisplay <> 1 //000
	THEN
	//Then the request from the client is just a basic component, 
	// so from the basic component declared on the PLC_PRG declaration part the program delivers the results
	
	//The temporal Value field gets the actual value of the request from the basicComponent object
	rDisplayValue := basicComponent.getValue();
	//The temporal Description field gets the actual value of the request from the basicComponent object
	sDisplayDescription := basicComponent.getDescription();
	//The temporal state of the display is set to 1, this will avoid processing duplicate requests
	iTempDisplay := 1;
END_IF

//If the user has chosen only Decoration A AND iTempDisplay is different to this concrete state of 2,
IF bDecorA AND NOT bDecorB AND NOT bDecorC AND iTempDisplay <> 2 //100
	THEN
	//Then the request from the client is a basic component with Decoration A, 
	// so from the basic component declared on the PLC_PRG declaration part the program delivers the results
	
	//First a ConcreteDecoratorA object must be created passing as an argument the basicComponent object
	ptrDecorA := __NEW(ConcreteDecoratorA(tempInputComponent := basicComponent));
	//The temporal Value field gets the actual value of the request from the ConcreteDecoratorA object
	rDisplayValue := ptrDecorA^.getValue();
	//The temporal Description field gets the actual value of the request from the ConcreteDecoratorA object
	sDisplayDescription := ptrDecorA^.getDescription();
	//The temporal state of the display is set to 2, this will avoid processing duplicate requests
	iTempDisplay := 2;
	//Now the ConcreteDecoratorA object is destroyed to free memory
	__DELETE(ptrDecorA);
END_IF

//If the user has chosen Decorations A and B AND iTempDisplay is different to this concrete state of 3,
IF bDecorA AND bDecorB AND NOT bDecorC AND iTempDisplay <> 3 //110
	THEN
	//Then the request from the client is just a basic component, 
	// so from the basic component declared on the PLC_PRG declaration part the program delivers the results
	
	//First a ConcreteDecoratorA object must be created passing as an argument the basicComponent object
	ptrDecorA := __NEW(ConcreteDecoratorA(tempInputComponent := basicComponent));
	//Then a ConcreteDecoratorB object must be created passing as an argument the ConcreteDecoratorA object
	ptrDecorB := __NEW(ConcreteDecoratorB(tempInputComponent := ptrDecorA^));
	//The temporal Value field gets the actual value of the request from the ConcreteDecoratorB object
	rDisplayValue := ptrDecorB^.getValue();
	//The temporal Description field gets the actual value of the request from the ConcreteDecoratorB object
	sDisplayDescription := ptrDecorB^.getDescription();
	//The temporal state of the display is set to 3, this will avoid processing duplicate requests
	iTempDisplay := 3;
	//Now the ConcreteDecoratorA object is destroyed to free memory
	__DELETE(ptrDecorA);
	//Now the ConcreteDecoratorB object is destroyed to free memory
	__DELETE(ptrDecorB);
END_IF

//If the user has chosen Decorations A, B and C AND iTempDisplay is different to this concrete state of 4,
IF bDecorA AND bDecorB AND bDecorC AND iTempDisplay <> 4 //111
	THEN
	//Then the request from the client is just a basic component, 
	// so from the basic component declared on the PLC_PRG declaration part the program delivers the results
	
	//First a ConcreteDecoratorA object must be created passing as an argument the basicComponent object
	ptrDecorA := __NEW(ConcreteDecoratorA(tempInputComponent := basicComponent));
	//Then a ConcreteDecoratorB object must be created passing as an argument the ConcreteDecoratorA object
	ptrDecorB := __NEW(ConcreteDecoratorB(tempInputComponent := ptrDecorA^));
	//Then a ConcreteDecoratorC object must be created passing as an argument the ConcreteDecoratorB object
	ptrDecorC := __NEW(ConcreteDecoratorC(tempInputComponent := ptrDecorB^));
	//The temporal Value field gets the actual value of the request from the ConcreteDecoratorC object
	rDisplayValue := ptrDecorC^.getValue();
	//The temporal Description field gets the actual value of the request from the ConcreteDecoratorC object
	sDisplayDescription := ptrDecorC^.getDescription();
	//The temporal state of the display is set to 4, this will avoid processing duplicate requests
	iTempDisplay := 4;
	//Now the ConcreteDecoratorA object is destroyed to free memory
	__DELETE(ptrDecorA);
	//Now the ConcreteDecoratorB object is destroyed to free memory
	__DELETE(ptrDecorB);
	//Now the ConcreteDecoratorC object is destroyed to free memory
	__DELETE(ptrDecorC);
END_IF

//If the user has chosen Decorations A and C AND iTempDisplay is different to this concrete state of 2,
IF bDecorA AND NOT bDecorB AND bDecorC AND iTempDisplay <> 5 //101
	THEN
	//Then the request from the client is just a basic component, 
	// so from the basic component declared on the PLC_PRG declaration part the program delivers the results
	
	//First a ConcreteDecoratorA object must be created passing as an argument the basicComponent object
	ptrDecorA := __NEW(ConcreteDecoratorA(tempInputComponent := basicComponent));
	//Then a ConcreteDecoratorC object must be created passing as an argument the ConcreteDecoratorA object
	ptrDecorC := __NEW(ConcreteDecoratorC(tempInputComponent := ptrDecorA^));
	//The temporal Value field gets the actual value of the request from the ConcreteDecoratorC object
	rDisplayValue := ptrDecorC^.getValue();
	//The temporal Description field gets the actual value of the request from the ConcreteDecoratorC object
	sDisplayDescription := ptrDecorC^.getDescription();
	//The temporal state of the display is set to 5, this will avoid processing duplicate requests
	iTempDisplay := 5;
	//Now the ConcreteDecoratorA object is destroyed to free memory
	__DELETE(ptrDecorA);
	//Now the ConcreteDecoratorC object is destroyed to free memory
	__DELETE(ptrDecorC);
END_IF

//If the user has chosen only Decoration B AND iTempDisplay is different to this concrete state of 6,
IF NOT bDecorA AND bDecorB AND NOT bDecorC AND iTempDisplay <> 6 //010
	THEN
	//Then the request from the client is just a basic component, 
	// so from the basic component declared on the PLC_PRG declaration part the program delivers the results
	
	//First a ConcreteDecoratorB object must be created passing as an argument the basicComponent object
	ptrDecorB := __NEW(ConcreteDecoratorB(tempInputComponent := basicComponent));
	//The temporal Value field gets the actual value of the request from the ConcreteDecoratorB object
	rDisplayValue := ptrDecorB^.getValue();
	//The temporal Description field gets the actual value of the request from the ConcreteDecoratorB object
	sDisplayDescription := ptrDecorB^.getDescription();
	//The temporal state of the display is set to 6, this will avoid processing duplicate requests
	iTempDisplay := 6;
	//Now the ConcreteDecoratorB object is destroyed to free memory
	__DELETE(ptrDecorB);
END_IF

//If the user has chosen Decorations B and C AND iTempDisplay is different to this concrete state of 7,
IF NOT bDecorA AND bDecorB AND bDecorC AND iTempDisplay <> 7 //011
	THEN
	//Then the request from the client is just a basic component, 
	// so from the basic component declared on the PLC_PRG declaration part the program delivers the results
	
	//First a ConcreteDecoratorB object must be created passing as an argument the basicComponent object
	ptrDecorB := __NEW(ConcreteDecoratorB(tempInputComponent := basicComponent));
	//Then a ConcreteDecoratorC object must be created passing as an argument the ConcreteDecoratorB object
	ptrDecorC := __NEW(ConcreteDecoratorC(tempInputComponent := ptrDecorB^));
	//The temporal Value field gets the actual value of the request from the ConcreteDecoratorC object
	rDisplayValue := ptrDecorC^.getValue();
	//The temporal Description field gets the actual value of the request from the ConcreteDecoratorC object
	sDisplayDescription := ptrDecorC^.getDescription();
	//The temporal state of the display is set to 7, this will avoid processing duplicate requests
	iTempDisplay := 7;
	//Now the ConcreteDecoratorB object is destroyed to free memory
	__DELETE(ptrDecorB);
	//Now the ConcreteDecoratorC object is destroyed to free memory
	__DELETE(ptrDecorC);
END_IF

//If the user has chosen only Decoration C AND iTempDisplay is different to this concrete state of 8,
IF NOT bDecorA AND NOT bDecorB AND bDecorC AND iTempDisplay <> 8 //001
	THEN
	//Then the request from the client is just a basic component, 
	// so from the basic component declared on the PLC_PRG declaration part the program delivers the results
	
	//First a ConcreteDecoratorC object must be created passing as an argument the basicComponent object
	ptrDecorC := __NEW(ConcreteDecoratorC(tempInputComponent := basicComponent));
	//The temporal Value field gets the actual value of the request from the ConcreteDecoratorC object
	rDisplayValue := ptrDecorC^.getValue();
	//The temporal Description field gets the actual value of the request from the ConcreteDecoratorC object
	sDisplayDescription := ptrDecorC^.getDescription();
	//The temporal state of the display is set to 8, this will avoid processing duplicate requests
	iTempDisplay := 8;
	//Now the ConcreteDecoratorC object is destroyed to free memory
	__DELETE(ptrDecorC);
END_IF
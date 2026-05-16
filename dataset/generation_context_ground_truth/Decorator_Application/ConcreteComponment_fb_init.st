VAR
	//String field to store the description of the object
	sDescription : STRING;
	//Real field to store the value of the object
	rValue : REAL;
END_VAR

//Sets the default description for the objects of this class
THIS^.sDescription := 'Plain Component';
//Sets the default value for the objects of this class
THIS^.rValue := 4.0;
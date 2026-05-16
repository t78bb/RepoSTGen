//Illustrative method of the pattern
METHOD getDescription : STRING
VAR_INPUT
END_VAR
VAR_OUTPUT
END_VAR
VAR
	//String field to store the description of the object
	sDescription : STRING;
	//Real field to store the value of the object
	rValue : REAL;
END_VAR


//Description of the plain object is given
getDescription := This^.sDescription;
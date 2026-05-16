//Illustrative method of the pattern
METHOD getValue : REAL
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

//Assume we are going to calculate the cost os the object.
//The plain value (without extra decoration) is given
getValue := THIS^.rValue;
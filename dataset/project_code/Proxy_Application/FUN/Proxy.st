{attribute 'enable_dynamic_creation'}
FUNCTION_BLOCK Proxy IMPLEMENTS  Subject_Interface
VAR_INPUT
END_VAR
VAR_OUTPUT
END_VAR
VAR
	//Pointer to store the reference to the subject being protected
	refToRealSubject : POINTER TO Realsubject;
	//Last value of password entered by the client in the visualization element
	iTempPassword : INT;
END_VAR
VAR_STAT
	//Default password value for the request to be accepted
	iRealPassword : INT := 1234;
END_VAR
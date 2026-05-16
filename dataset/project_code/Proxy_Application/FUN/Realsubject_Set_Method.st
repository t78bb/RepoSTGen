METHOD Set_Method 
VAR_INPUT
	//Value to be set on the iProp varible of realSubjectInstance
	num : INT;
    	//Variable to get and set values
	iProp: INT;
END_VAR

//Stores the value of the caller object on iProp variable. 

THIS^.iProp := num;
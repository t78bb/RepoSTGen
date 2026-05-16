{attribute 'qualified_only'}
VAR_GLOBAL CONSTANT
	//Constant variable to determine the size of the observerList array.
	//This variable is the MAXIMUM number of observer objects that can be subscribed to the subject
	C_MAX_OBSERVER_NUM : INT := 10;
	//Pointer to a null Observer_Interface object.
	//This pointer is used to validate the addresses to be used. These addresses must to be <> than this null pointer to have effect in the code
	nullPointerToObserver : Observer_Interface;
END_VAR
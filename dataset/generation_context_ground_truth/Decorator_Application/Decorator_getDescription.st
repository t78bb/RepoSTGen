VAR
	//Variable to save the state of the concrete component to be decorated
	tempComponent : Component_Interface;
	//String variable to save the Description of the component
	sDescription : STRING;
	//Real variable to save the Value of the component
	rValue : REAL;
END_VAR

//Outputs the description of the component to be decorated tempComponent. If tempComponent is not an undecorated component (plain object)
// it means the program has to do at least 2 decorations. Then is going to output the previous decoration complete description
// to be used by the next decorator.
getDescription := THIS^.tempComponent.getDescription();
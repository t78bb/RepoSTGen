//Illustrative method of the pattern
METHOD getValue : REAL
VAR_INPUT
END_VAR
VAR_OUTPUT
END_VAR
VAR
	//Variable to save the state of the concrete component to be decorated
	tempComponent : Component_Interface;
	//String variable to save the Description of the component
	sDescription : STRING;
	//Real variable to save the Value of the component
	rValue : REAL;
END_VAR



//Outputs the cost of the component to be decorated tempComponent. If tempComponent is not an undecorated component (plain object)
// it means the program has to do at least 2 decorations. Then is going to output the previous decoration complete value
// to be used by the next decorator.
getValue := tempComponent.getValue();
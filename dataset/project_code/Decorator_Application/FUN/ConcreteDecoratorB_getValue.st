//Illustrative method of the pattern
METHOD getValue : REAL
VAR_INPUT
	//Reference to store the component to be decorated
	tempInputComponent : Component_Interface;
END_VAR
VAR_OUTPUT
END_VAR
VAR
END_VAR


//Outputs the decorated cost of the component by obtaining the cost of the component to be decorated 
// stored in tempComponent.getValue() and then adds the decoration value (0.35 as example)
getValue := tempComponent.getValue() + THIS^.rValue;
//Illustrative method of the pattern
METHOD getDescription : STRING
VAR_INPUT
	//Reference to store the component to be decorated
	tempInputComponent : Component_Interface;
END_VAR


//Outputs the decorated description of the component by obtaining the description of the component
// to be decorated stored in tempComponet.getDescription() and then concatenates the decoration
// description( ' Decorator A' as example)
getDescription :=CONCAT(THIS^.tempComponent.getDescription() , THIS^.sDescription);

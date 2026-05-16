VAR
END_VAR

//Outputs the decorated description of the component by obtaining the description of the component
// to be decorated stored in tempComponet.getDescription() and then concatenates the decoration
// description( ' Decorator C' as example)
getDescription :=CONCAT(THIS^.tempComponent.getDescription() , THIS^.sDescription);
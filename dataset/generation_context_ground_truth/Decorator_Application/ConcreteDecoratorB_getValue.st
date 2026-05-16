VAR
END_VAR


//Outputs the decorated cost of the component by obtaining the cost of the component to be decorated 
// stored in tempComponent.getValue() and then adds the decoration value (0.35 as example)
getValue := tempComponent.getValue() + THIS^.rValue;
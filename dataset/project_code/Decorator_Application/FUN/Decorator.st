{attribute 'enable_dynamic_creation'}
//This class mainteins the reference to a ConcreteComponent object and works as an interface 
// for its subclasses to decorate the ConcreteComponent 
FUNCTION_BLOCK Decorator IMPLEMENTS Component_Interface
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

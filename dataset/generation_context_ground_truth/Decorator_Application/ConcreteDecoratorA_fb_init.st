
//Calls the constructor (fb_init) in its SUPER class (Decorator)
// in order to pass the component to be decorated to the Decorator constructor.
SUPER^.fb_init(TRUE, TRUE, tempInputComponent);
//Sets the default description for the objects of this class
THIS^.sDescription := ' Decorator A';
//Sets the default value for the objects of this class
THIS^.rValue := 0.5;
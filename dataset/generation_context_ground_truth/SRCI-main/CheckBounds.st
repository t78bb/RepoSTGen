
// Implicitly generated code : Only an Implementation suggestion
{noflow}
IF  index < lower THEN
  CheckBounds := lower;
ELSIF  index > upper THEN
  CheckBounds := upper;
ELSE  
  CheckBounds := index;
END_IF
{flow}
VAR
		//Local variable to join together and store the pieces of String
	tempString: STRING;
END_VAR

//tempString joins together "Main Part" and "Part 1" of the Product object
tempString := CONCAT(THIS^.mainPart , THIS^.part1);
//tempString joins together its current value and "Part 2" of the Product object
tempString := CONCAT(tempString , THIS^.part2);
//tempString joins together its current value and "Part 3" of the Product object
tempString := CONCAT(tempString , THIS^.part3);
//The final result is sent as the output of this method
toString := tempString;
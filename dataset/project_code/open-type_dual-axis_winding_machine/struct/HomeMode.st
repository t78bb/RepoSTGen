TYPE HomeMode :
(
	FAST_ZERO := 0,//Move with fast velocity onto the zero position
	FAST_BSLOW_STOP_S := 1,//Move with fast velocity onto the reference switch; invert and move with slow velocity out of the reference switch; stop;execute “set position” 
	FAST_SLOW_STOP_S := 2,//Move with fast velocity onto the reference switch; move with slow velocity out of the reference switch; stop;execute “set position” 
	FAST_BSLOW_I_STOP_S := 3,//Move with fast velocity onto the reference switch; invert and move with slow velocity out of the reference switch; wait for the index pulse; stop;execute “set position”  
	FAST_SLOW_I_STOP_S := 4//Move with fast velocity onto the reference switch; move with slow velocity out of the reference switch; wait for the index pulse; stop;execute “set position” 
);
END_TYPE
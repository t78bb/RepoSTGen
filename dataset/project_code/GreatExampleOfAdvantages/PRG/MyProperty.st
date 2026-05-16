(*this is the very best example of using auto MQTT Topics!!!
All topics are made only by the structure and names of the instances of the FBs!!!
no topic needs to be tippt anywhere and anymore!

Create new FBs and use auto topics of this base!

everything is createt and topic structs can be easy changed by moving FBs instances!

here ar the topics and payloads to controll your home!

HomeControl/Application/Receive/MyProperty/Home/TopFloor/SleepingRoom/Lamp1 --> Switch Lamp On
HomeControl/Application/Receive/MyProperty/Home/TopFloor/SleepingRoom/Lamp1 --> Switch Lamp Off

HomeControl/Application/Receive/MyProperty/Home/TopFloor/SleepingRoom/Temperature --> Set:23.3

HomeControl/Application/Receive/MyProperty/Home/TopFloor/MainBath/Lamp1 --> Switch Lamp On
HomeControl/Application/Receive/MyProperty/Home/TopFloor/MainBath/Lamp1 --> Switch Lamp Off
HomeControl/Application/Receive/MyProperty/Home/TopFloor/MainBath/Lamp2 --> Switch Lamp On
HomeControl/Application/Receive/MyProperty/Home/TopFloor/MainBath/Lamp2 --> Switch Lamp Off
HomeControl/Application/Receive/MyProperty/Home/TopFloor/MainBath/Lamp3 --> Switch Lamp On
HomeControl/Application/Receive/MyProperty/Home/TopFloor/MainBath/Lamp3 --> Switch Lamp Off

HomeControl/Application/Receive/MyProperty/Home/TopFloor/MainBath/Temperature --> Set:22.1

HomeControl/Application/Receive/MyProperty/Home/GroundFloor/GuestBath/Lamp1 --> Switch Lamp On
HomeControl/Application/Receive/MyProperty/Home/GroundFloor/GuestBath/Lamp1 --> Switch Lamp Off

HomeControl/Application/Receive/MyProperty/Home/GroundFloor/GuestBath/Temperature --> Set:20.8

HomeControl/Application/Receive/MyProperty/Home/GroundFloor/LivingRoom/Lamp1 --> Switch Lamp On
HomeControl/Application/Receive/MyProperty/Home/GroundFloor/LivingRoom/Lamp1 --> Switch Lamp Off
HomeControl/Application/Receive/MyProperty/Home/GroundFloor/LivingRoom/Lamp2 --> Switch Lamp On
HomeControl/Application/Receive/MyProperty/Home/GroundFloor/LivingRoom/Lamp2 --> Switch Lamp Off
HomeControl/Application/Receive/MyProperty/Home/GroundFloor/LivingRoom/Lamp3 --> Switch Lamp On
HomeControl/Application/Receive/MyProperty/Home/GroundFloor/LivingRoom/Lamp3 --> Switch Lamp Off

HomeControl/Application/Receive/MyProperty/Home/GroundFloor/LivingRoom/Temperature  --> Set:21.3

*)


PROGRAM MyProperty
VAR
	Collector:MQTT.CallbackCollector;
	Home:Home;
	MQTT:MQTT_STUFF;
END_VAR

Home();
MQTT();
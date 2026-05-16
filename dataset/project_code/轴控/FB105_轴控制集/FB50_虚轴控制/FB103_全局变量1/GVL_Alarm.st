VAR_GLOBAL
	(*轴类*)
	HMI_b调模A轴报警 		AT %MX200.0: BOOL;
	HMI_b调模B轴报警 		AT %MX200.1: BOOL;
	HMI_b送面料轴报警 		AT %MX200.2: BOOL;
	HMI_b取面料轴报警 		AT %MX200.3: BOOL;
	HMI_b横移A轴报警 		AT %MX200.4: BOOL;
	HMI_b升降A轴报警 		AT %MX200.5: BOOL;	
	HMI_b横移B轴报警 		AT %MX200.6: BOOL;
	HMI_b升降B轴报警 		AT %MX200.7: BOOL;
	HMI_b出盒轴报警 		AT %MX201.0: BOOL;
	HMI_b铲灰板轴报警 		AT %MX201.1: BOOL;
	HMI_b包面纸轴报警 		AT %MX201.2: BOOL;
	HMI_b上包底轴报警 		AT %MX201.3: BOOL;
	HMI_b折边轴报警 		AT %MX201.4: BOOL;
	
	(*气类*)
	HMI_b取料气缸报警 		AT %MX201.5: BOOL;
	HMI_b纠偏气缸报警 		AT %MX201.6: BOOL;
	HMI_b挡料定位气缸报警 	AT %MX201.7: BOOL;
	HMI_b翻板气缸报警 		AT %MX202.0: BOOL;
	HMI_b侧压紧气缸报警 	AT %MX202.1: BOOL;
	HMI_b左A包底气缸报警 	AT %MX202.2: BOOL;	
	HMI_b右B包底气缸报警 	AT %MX202.3: BOOL;
	HMI_b上包底气缸报警 	AT %MX202.4: BOOL;
	
	HMI_b下包底气缸报警 	AT %MX202.5: BOOL;
	HMI_b出料推盒气缸报警 	AT %MX202.6: BOOL;
	HMI_b包盒口升降气缸报警 AT %MX202.7: BOOL;
	HMI_b包盒口下压气缸报警 AT %MX203.0: BOOL;	
	HMI_b翻底板气缸报警 	AT %MX203.1: BOOL;
	HMI_b推底板气缸报警 	AT %MX203.2: BOOL;
	HMI_b模组吸底板气缸报警 AT %MX203.3: BOOL;
	
	HMI_b包边纠偏上下气缸报警 AT %MX203.4: BOOL;
	HMI_b包边纠偏左右气缸报警 AT %MX203.5: BOOL;
	HMI_b包边压料气缸报警 	AT %MX203.6: BOOL;
	HMI_b折边上托气缸报警 	AT %MX203.7: BOOL;
	HMI_b包边铲边气缸报警	AT %MX204.0: BOOL;
	
	HMI_b吸底板真空报警 	AT %MX204.1: BOOL;  
	HMI_b取面板真空报警 	AT %MX204.2: BOOL;
	HMI_bA模吸底板真空报警  AT %MX204.3: BOOL;
	HMI_bA模吸面板真空报警  AT %MX204.4: BOOL;
	HMI_bB模吸底板真空报警  AT %MX204.5: BOOL;
    HMI_bB模吸面板真空报警  AT %MX204.6: BOOL;	
	
	(*其它类*)
	HMI_b设备未回零启动报警 AT %MX204.7: BOOL;
	HMI_b设备在手动模式启动报警 AT %MX205.0: BOOL;
	HMI_b急停报警 			AT %MX205.1: BOOL;
	HMI_b总气压报警 		AT %MX205.2: BOOL;
	
	HMI_b折边工位入料光纤检测异常报警 AT %MX205.3: BOOL;
	HMI_b取料工位入料光纤检测异常报警 AT %MX205.4: BOOL;
			
END_VAR
VAR_GLOBAL
	
(****************************************************输入****************************************************)
DI_折边工位入料感应 				AT %MX0.0:BOOL;
DI_取料工位入料感应 				AT %MX0.1:BOOL;
DI_手自动选择开关 			        AT %MX0.2:BOOL;
DI_启动按钮 			            AT %MX0.3:BOOL;
DI_停止按钮 	                    AT %MX0.4:BOOL;
DI_复位按钮 					    AT %MX0.5:BOOL;
DI_急停按钮 				        AT %MX0.6:BOOL;

DI_总气压检测			            AT %MX1.0:BOOL;
DI_取面板真空检测 			        AT %MX1.1:BOOL;
DI_吸底板真空检测 			        AT %MX1.2:BOOL;
DI_A吸底板真空检测 					AT %MX1.3:BOOL;
DI_A吸面板真空检测 				    AT %MX1.4:BOOL;
DI_B吸底板真空检测				    AT %MX1.5:BOOL;
DI_B吸面板真空检测 			        AT %MX1.6:BOOL;

DI_取料上下气缸原点 			    AT %MX2.0:BOOL;
DI_取料上下气缸动点 			    AT %MX2.1:BOOL;
DI_入料纠偏气缸原点 			    AT %MX2.2:BOOL;
DI_入料纠偏气缸动点  				AT %MX2.3:BOOL;
DI_翻板气缸原点 				    AT %MX2.4:BOOL;
DI_翻板气缸动点  				    AT %MX2.5:BOOL;
DI_左A包底气缸原点 				    AT %MX2.6:BOOL;
DI_右B包底气缸原点 				    AT %MX2.7:BOOL;

DI_上包底气缸原点			        AT %MX3.0:BOOL;
DI_出料推盒气缸原点 			    AT %MX3.1:BOOL;
DI_出料推盒气缸动点	                AT %MX3.2:BOOL;
DI_包盒口升降气缸原点 		        AT %MX3.3:BOOL;
DI_包盒口升降气缸动点 		        AT %MX3.4:BOOL;
DI_包盒口下压气缸原点 		        AT %MX3.5:BOOL;
DI_包盒口下压气缸动点 			    AT %MX3.6:BOOL;

DI_推底板气缸原点 				    AT %MX4.0:BOOL;
DI_推底板气缸动点 				    AT %MX4.1:BOOL;
DI_翻底板气缸原点 					AT %MX4.2:BOOL;
DI_翻底板气缸动点 				    AT %MX4.3:BOOL;
DI_模组吸底板气缸原点 				AT %MX4.4:BOOL;

DI_调模A步进原点 					AT %MX5.0:BOOL;
DI_调模A步进限位 				    AT %MX5.1:BOOL;
DI_调模B步进原点 				    AT %MX5.2:BOOL;
DI_调模B步进限位 				    AT %MX5.3:BOOL;

(****************************************************输出****************************************************)
(*取料工位*)
DO_取料气缸 					    AT %MX50.0:BOOL;
DO_纠偏气缸 						AT %MX50.1:BOOL;
DO_挡料定位气缸 					AT %MX50.2:BOOL;
(*成型工位*)
DO_翻板气缸							AT %MX50.3:BOOL;
DO_侧压紧气缸 					    AT %MX50.4:BOOL;
DO_左A包底气缸 					    AT %MX50.5:BOOL;
DO_右B包底气缸 					    AT %MX50.6:BOOL;
DO_上包底气缸 						AT %MX50.7:BOOL;

DO_下包底气缸 					    AT %MX51.0:BOOL;
(*出盒工位*)
DO_出料推盒气缸 					AT %MX51.1:BOOL;
DO_包盒口升降气缸					AT %MX51.2:BOOL;
DO_包盒口下压气缸 					AT %MX51.3:BOOL;
(*送底板工位*)
DO_翻底板气缸 						AT %MX51.4:BOOL;
DO_推底板气缸 					    AT %MX51.5:BOOL;
DO_模组吸底板气缸 					AT %MX51.6:BOOL;
(*折边工位*)
DO_包边纠偏上下气缸 				AT %MX52.0:BOOL;
DO_包边纠偏左右气缸 				AT %MX52.1:BOOL;
DO_包边压料气缸 					AT %MX52.2:BOOL;
DO_折边上托气缸 					AT %MX52.3:BOOL;
DO_包边铲边气缸 				    AT %MX52.4:BOOL;

DO_吸底板真空 			            AT %MX53.0:BOOL;
DO_取面板真空 			            AT %MX53.1:BOOL;
DO_A模吸底板真空 				    AT %MX53.2:BOOL;
DO_A模吸面板真空 				    AT %MX53.3:BOOL;
DO_B模吸底板真空 			        AT %MX53.4:BOOL;
DO_B模吸面板真空 			        AT %MX53.5:BOOL;

DO_三色灯红 				        AT %MX54.0:BOOL;
DO_三色灯黄 				        AT %MX54.1:BOOL;
DO_三色灯绿 					    AT %MX54.2:BOOL;
DO_三色灯蜂鸣器					    AT %MX54.3:BOOL;
DO_真空泵 						    AT %MX54.4:BOOL;
DO_出料皮带电机 					AT %MX54.5:BOOL;
DO_升降A轴抱闸释放 					AT %MX54.6:BOOL;
DO_升降B轴抱闸释放					AT %MX54.7:BOOL;


END_VAR
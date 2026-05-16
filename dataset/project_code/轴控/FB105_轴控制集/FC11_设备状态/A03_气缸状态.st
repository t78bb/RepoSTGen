IF DI_取料上下气缸原点 AND DI_入料纠偏气缸原点 AND DI_翻板气缸原点 AND DI_左A包底气缸原点 AND DI_右B包底气缸原点 AND
	DI_上包底气缸原点 AND DI_出料推盒气缸原点 AND DI_包盒口升降气缸原点 AND DI_包盒口下压气缸原点 AND DI_推底板气缸原点 AND
	 DI_翻底板气缸原点 AND DI_模组吸底板气缸原点 THEN
	 b所有气缸原位OK:=TRUE;
	 ELSE
	 b所有气缸原位OK:=FALSE;	 
END_IF

IF NOT DO_取料气缸 AND NOT DO_纠偏气缸 AND NOT DO_挡料定位气缸 AND NOT DO_翻板气缸 AND NOT DO_侧压紧气缸 AND NOT DO_左A包底气缸 AND
	NOT DO_右B包底气缸 AND NOT DO_上包底气缸 AND NOT DO_下包底气缸 AND NOT DO_出料推盒气缸 AND NOT DO_包盒口升降气缸 AND
	NOT DO_包盒口下压气缸 AND NOT DO_翻底板气缸 AND NOT DO_推底板气缸 AND NOT DO_模组吸底板气缸 AND NOT DO_包边纠偏上下气缸 AND 
	NOT DO_包边纠偏左右气缸 AND NOT DO_包边压料气缸 AND NOT DO_折边上托气缸 AND NOT DO_包边铲边气缸 AND NOT DO_吸底板真空 AND 
	NOT DO_取面板真空 AND NOT DO_A模吸底板真空 AND NOT DO_A模吸面板真空 AND NOT DO_B模吸底板真空 AND NOT DO_B模吸面板真空 THEN
	b所有气缸关闭OK:=TRUE;
	ELSE
	b所有气缸关闭OK:=FALSE;	
END_IF
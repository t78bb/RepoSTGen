//从站通讯状态
pSlave := EtherCAT_Master_Leadshine.FirstSlave; //建立指针，指向主站后第一个从站
No_Slave:=0;
WHILE pSlave <> 0 DO 
  No_Slave:=No_Slave+1;
  pSlave^(); //获取当前从站状态内容
IF pSlave^.wState <>ETC_SLAVE_STATE.ETC_SLAVE_OPERATIONAL THEN //
    ERROR[No_Slave]:=1;   //对应关系 ERROR[1]=1有错误   ERROR[1] 1号从站、ERROR[2] 2号从站,建立的数组元素个数等于从站个数
ELSE
    ERROR[No_Slave]:=0;
END_IF
pSlave := pSlave^.NextInstance; //指向下个从站，结尾为空，跳出循环
END_WHILE 


//EtherCAT主站复位
EtherCAT_Master_Leadshine(
	xRestart:= bEtcReset, 
	xStopBus:= , 
	xConfigFinished=> , 
	xDistributedClockInSync=> , 
	xError=> , 
	xSyncInWindow=> );

IF EtherCAT_Master_Leadshine.xConfigFinished AND EtherCAT_Master_Leadshine.xDistributedClockInSync THEN
	FB_AxisControl_AxisVirtual.ReStartSlaveEx:=TRUE;
	FB_AxisControl_调模A轴.ReStartSlaveEx:=TRUE;
	FB_AxisControl_调模B轴.ReStartSlaveEx:=TRUE;
	FB_AxisControl_送面料轴.ReStartSlaveEx:=TRUE;
	FB_AxisControl_取面料轴.ReStartSlaveEx:=TRUE;
	FB_AxisControl_横移A轴.ReStartSlaveEx:=TRUE;
	FB_AxisControl_升降A轴.ReStartSlaveEx:=TRUE;
	FB_AxisControl_横移B轴.ReStartSlaveEx:=TRUE;
	FB_AxisControl_升降B轴.ReStartSlaveEx:=TRUE;
	FB_AxisControl_出盒轴.ReStartSlaveEx:=TRUE;
	FB_AxisControl_铲灰板轴.ReStartSlaveEx:=TRUE;
	FB_AxisControl_包面纸轴.ReStartSlaveEx:=TRUE;
	FB_AxisControl_上包底轴.ReStartSlaveEx:=TRUE;
	FB_AxisControl_折边轴.ReStartSlaveEx:=TRUE;
	IF FB_AxisControl_AxisVirtual.ReStartSlaveDone AND FB_AxisControl_调模A轴.ReStartSlaveDone AND FB_AxisControl_调模B轴.ReStartSlaveDone AND 
        FB_AxisControl_送面料轴.ReStartSlaveDone AND FB_AxisControl_取面料轴.ReStartSlaveDone AND FB_AxisControl_横移A轴.ReStartSlaveDone AND
		 FB_AxisControl_升降A轴.ReStartSlaveDone AND FB_AxisControl_横移B轴.ReStartSlaveDone AND FB_AxisControl_升降B轴.ReStartSlaveDone AND
		  FB_AxisControl_出盒轴.ReStartSlaveDone AND FB_AxisControl_铲灰板轴.ReStartSlaveDone AND FB_AxisControl_包面纸轴.ReStartSlaveDone AND
		   FB_AxisControl_上包底轴.ReStartSlaveDone AND FB_AxisControl_折边轴.ReStartSlaveDone THEN
	      bEtcReset:=FALSE;
	END_IF
END_IF




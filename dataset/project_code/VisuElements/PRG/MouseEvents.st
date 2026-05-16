PROGRAM Node
VAR
	xNodeExpand   : BOOL;
	NodeDblClick  : TON;
	tNodeDblClick : TIME := T#500MS; (* the time to wait for the second click *)
	xNodeClick    : BOOL;
	xNodeClickOld : BOOL;
	iNodeState    : INT := 1;
	xNodeSelected : BOOL;
END_VAR

(* This program ellapses/collapses a node, by dozble clicking the first node *)

CASE iNodeState OF

	1: (* first click on the node
		  the first click toggles the xNodeClick variable to true*)
		IF xNodeClick AND NOT xNodeClickOld THEN
			NodeDblClick(IN:=TRUE, PT:=tNodeDblClick);
			iNodeState    := 2;
		END_IF
	
	2: (* The second click expands respectively collapses the Node *)
		NodeDblClick();
		(* the time for the second click is elapsed*)
		IF NodeDblClick.Q THEN
			NodeDblClick(IN:=FALSE);
			xNodeClick := xNodeClickOld := FALSE;
			iNodeState := 1;
		ELSE
		(* check for the second click,
			when xNodeClick is false, the user has clicked the second time, because xNodeClick is toggled*)
			IF NOT xNodeClick AND xNodeClickOld THEN
				NodeDblClick(IN:=FALSE);
				xNodeExpand := NOT xNodeExpand;
				iNodeState  := 1;
			END_IF
		END_IF
END_CASExNodeClickOld := xNodeClick;

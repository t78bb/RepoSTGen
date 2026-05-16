VAR
    NodeDblClick : TON;
    xNodeClickOld : BOOL;
    iNodeState : INT := 1;
END_VAR

(* This function block handles double-click expansion/collapse of a node *)

CASE iNodeState OF

    1: (* Wait for first click *)
        IF xNodeClick AND NOT xNodeClickOld THEN
            NodeDblClick(IN:=TRUE, PT:=tDblClickTime);
            iNodeState := 2;
            xNodeSelected := TRUE;
        END_IF

    2: (* Wait for second click or timeout *)
        NodeDblClick();
        IF NodeDblClick.Q THEN
            (* Timeout - single click, reset *)
            NodeDblClick(IN:=FALSE);
            xNodeClickOld := FALSE;
            iNodeState := 1;
            xNodeSelected := FALSE;
        ELSIF NOT xNodeClick AND xNodeClickOld THEN
            (* Second click detected - toggle expansion *)
            NodeDblClick(IN:=FALSE);
            xNodeExpand := NOT xNodeExpand;
            iNodeState := 1;
            xNodeSelected := FALSE;
        END_IF
END_CASE

xNodeClickOld := xNodeClick;

VAR
    rRadians : REAL;
    rCos : REAL;
    rSin : REAL;
    rTranslatedX : REAL;
    rTranslatedY : REAL;
END_VAR

(* Convert angle from degrees to radians *)
rRadians := rAngle * 3.14159 / 180.0;

(* Calculate sine and cosine *)
rCos := COS(rRadians);
rSin := SIN(rRadians);

(* Translate point to origin (relative to center) *)
rTranslatedX := rPointX - rCenterX;
rTranslatedY := rPointY - rCenterY;

(* Apply rotation matrix *)
rRotatedX := rTranslatedX * rCos - rTranslatedY * rSin;
rRotatedY := rTranslatedX * rSin + rTranslatedY * rCos;

(* Translate back to original position *)
rRotatedX := rRotatedX + rCenterX;
rRotatedY := rRotatedY + rCenterY;

RotationCalculation := TRUE;  (* Return success *)

FUNCTION RotationCalculation : BOOL
VAR_INPUT
    rCenterX : REAL;    (* X coordinate of rotation center *)
    rCenterY : REAL;    (* Y coordinate of rotation center *)
    rAngle : REAL;      (* Rotation angle in degrees *)
    rPointX : REAL;     (* X coordinate of point to rotate *)
    rPointY : REAL;     (* Y coordinate of point to rotate *)
END_VAR

VAR_OUTPUT
    rRotatedX : REAL;   (* X coordinate after rotation *)
    rRotatedY : REAL;   (* Y coordinate after rotation *)
END_VAR

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

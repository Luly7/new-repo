CHARA   .BYTE   'a' ;
CHARB   .BYTE   'b' ;
TARGET  .SPACE  1 ;

START   ADR R1 CHARA ;
        ADR R2 TARGET ;
        STRB R1 [R2] ;
        SWI 1;
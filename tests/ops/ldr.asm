CHARA   .BYTE   'a' ;
CHARB   .BYTE   'b' ;
TARGET  .SPACE  1 ;
WORD1   .WORD   300 ;

START   ADR R1 WORD1 ;
        ADR R2 TARGET ;
        LDR R0 [R1] ;
        SWI 1 ;
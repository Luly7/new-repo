HUNDRED .WORD 100 ;
TARGET  .SPACE 4  ;

START:  MVI R1 100 ;
        ADR R2 TARGET ;
        STR R1 [R2] ;
        SWI 1 ;
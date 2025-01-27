START:  MVI R1 100 ;
        MVI R2 200 ;
        BL JUMP ;
        ADD R0 R1 R2 ;
        SWI 1 ;

JUMP   MVI R3 300 ;
        BX R5 ;
        SWI 1 ;
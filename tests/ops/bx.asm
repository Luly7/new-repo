START:  MVI R1 100 ;
        MVI R2 200 ;
        ADR R5 TARGET
        BX R5 ;
        ADD R3 R1 R2 ;
TARGET SUB R0 R2 R1 ;
        SWI 1 ;
        
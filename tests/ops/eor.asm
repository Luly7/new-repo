START   MVI R0 1 ;
        MVI R1 1 ;
        EOR R0 R1 Z ; should be 0
        MOV R2 Z ;
        MVI R0 0 ;
        MVI R1 1 ;
        EOR R0 R1 Z ; should be 1
        MOV R3 Z ;
        MVI R0 0 ;
        MVI R1 0 ;
        EOR R0 R1 Z ; should be 0
        MOV R4 Z ;
        SWI 1 ;
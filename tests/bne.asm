START   MVI R1 100 ;
        MVI R2 100 ;
        CMP R1 R2 ;
        BNE NOT_EQUAL ;
        MVI R0 1 ;
        SWI 1 ;
NOT_EQUAL MVI R0 0 ;
        SWI 1 ;
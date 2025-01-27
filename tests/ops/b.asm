START  MVI R1 100 ;
       MVI R2 200 ;
       B SU ;
       ADD R0 R1 R2 ;
SU     SUB R0 R2 R1 ;
END    SWI 1 ;

HUNDRED .WORD 100 ;
.BYTE 'a' ;
.SPACE 10 ;


ADR R1 HUNDRED ;
MVI R2 100 ;
MVI R3 100 ;
ADD R0 R2 R3 ;
SWI 1 ;
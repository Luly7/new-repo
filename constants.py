
USER_MODE = 0x01
KERNEL_MODE = 0x00

SYSTEM_CODES = {
    0: "Success",
    1: "Operation completed successfully",
    100: "Unknown error occurred",
    101: "No program loaded",
    102: "Memory allocation error",
    103: "Invalid instruction",
    104: "Division by zero",
    105: "Invalid memory access",
    106: "Stack overflow",
    107: "Stack underflow",
    108: "Invalid register",
    109: "File not found",
    110: "Out of bounds memory access",
}

instructions = {
    16: "ADD",
    17: "SUB",
    18: "MUL",
    19: "DIV",
    1:  "MOV",
    22: "MVI",
    0:  "ADR",
    2:  "STR",
    3:  "STRB",
    4:  "LDR",
    5:  "LDRB",
    7:  "B",
    21: "BL",
    6:  "BX",
    8:  "BNE",
    9:  "BGT",
    10: "BLT",
    11: "BEQ",
    12: "CMP",
    13: "AND",
    14: "ORR",
    15: 'EOR',
    20:  "SWI"
}
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// i=0
// BEGIN:
// if i==R1, goto end
// sum += R0
// i += 1
// GOTO BEGIN
// END:
// return
@i
M=0
@R2
M=0
(BEGIN)
@i
D=M
@R1
D=D-M
@END
D;JEQ
@R0
D=M
@R2
M=M+D
@i
M=M+1
@BEGIN
0;JMP

@END
0;JMP

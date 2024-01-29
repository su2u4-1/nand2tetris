// sum = 0
// (loop)
// sum = sum + R0
// R1 = R1 - 1
// if R1 == 0; goto f
// goto loop

// (f)
// R2 = sum
// (end)
// goto end

@R2
M=0
@R0
D=M
@R1
D=D-M
@ab
D;JLE
@ba
0;JMP

(ab)
@R1
D=M
@b
M=D
(loop0)
@R0
D=M
@R2
M=M+D
@b
M=M-1
D=M
@end
D;JLE
@loop0
0;JMP

(ba)
@R0
D=M
@b
M=D
(loop1)
@R1
D=M
@R2
M=M+D
@b
M=M-1
D=M
@end
D;JLE
@loop1
0;JMP

(end)
@end
0;JMP
@17
D=A
@SP
M=M+1
A=M-1
M=D
@17
D=A
@SP
M=M+1
A=M-1
M=D
@SP
A=M-1
D=M
A=A-1
D=D-M
@TRUE2
D;JEQ
@SP
M=M-1
A=M-1
M=0
@END2
0;JMP
(TRUE2)
@SP
M=M-1
A=M-1
M=-1
(END2)
@17
D=A
@SP
M=M+1
A=M-1
M=D
@16
D=A
@SP
M=M+1
A=M-1
M=D
@SP
A=M-1
D=M
A=A-1
D=D-M
@TRUE5
D;JEQ
@SP
M=M-1
A=M-1
M=0
@END5
0;JMP
(TRUE5)
@SP
M=M-1
A=M-1
M=-1
(END5)
@16
D=A
@SP
M=M+1
A=M-1
M=D
@17
D=A
@SP
M=M+1
A=M-1
M=D
@SP
A=M-1
D=M
A=A-1
D=D-M
@TRUE8
D;JEQ
@SP
M=M-1
A=M-1
M=0
@END8
0;JMP
(TRUE8)
@SP
M=M-1
A=M-1
M=-1
(END8)
@892
D=A
@SP
M=M+1
A=M-1
M=D
@891
D=A
@SP
M=M+1
A=M-1
M=D
@SP
A=M-1
D=M
A=A-1
D=D-M
@TRUE11
D;JGT
@SP
M=M-1
A=M-1
M=0
@END11
0;JMP
(TRUE11)
@SP
M=M-1
A=M-1
M=-1
(END11)
@891
D=A
@SP
M=M+1
A=M-1
M=D
@892
D=A
@SP
M=M+1
A=M-1
M=D
@SP
A=M-1
D=M
A=A-1
D=D-M
@TRUE14
D;JGT
@SP
M=M-1
A=M-1
M=0
@END14
0;JMP
(TRUE14)
@SP
M=M-1
A=M-1
M=-1
(END14)
@891
D=A
@SP
M=M+1
A=M-1
M=D
@891
D=A
@SP
M=M+1
A=M-1
M=D
@SP
A=M-1
D=M
A=A-1
D=D-M
@TRUE17
D;JGT
@SP
M=M-1
A=M-1
M=0
@END17
0;JMP
(TRUE17)
@SP
M=M-1
A=M-1
M=-1
(END17)
@32767
D=A
@SP
M=M+1
A=M-1
M=D
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@SP
A=M-1
D=M
A=A-1
D=D-M
@TRUE20
D;JLT
@SP
M=M-1
A=M-1
M=0
@END20
0;JMP
(TRUE20)
@SP
M=M-1
A=M-1
M=-1
(END20)
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@32767
D=A
@SP
M=M+1
A=M-1
M=D
@SP
A=M-1
D=M
A=A-1
D=D-M
@TRUE23
D;JLT
@SP
M=M-1
A=M-1
M=0
@END23
0;JMP
(TRUE23)
@SP
M=M-1
A=M-1
M=-1
(END23)
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@SP
A=M-1
D=M
A=A-1
D=D-M
@TRUE26
D;JLT
@SP
M=M-1
A=M-1
M=0
@END26
0;JMP
(TRUE26)
@SP
M=M-1
A=M-1
M=-1
(END26)
@57
D=A
@SP
M=M+1
A=M-1
M=D
@31
D=A
@SP
M=M+1
A=M-1
M=D
@53
D=A
@SP
M=M+1
A=M-1
M=D
@SP
A=M-1
D=M
A=A-1
D=D+M
@SP
M=M-1
A=M-1
M=D
@112
D=A
@SP
M=M+1
A=M-1
M=D
@SP
A=M-1
D=M
A=A-1
D=M-D
@SP
M=M-1
A=M-1
M=D
@SP
A=M-1
D=M
D=D-M
M=D-M
@SP
A=M-1
D=M
A=A-1
D=D&M
@SP
M=M-1
A=M-1
M=D
@82
D=A
@SP
M=M+1
A=M-1
M=D
@SP
A=M-1
D=M
A=A-1
D=D|M
@SP
M=M-1
A=M-1
M=D
@SP
A=M-1
M=!M
(END)
@END
0;JMP
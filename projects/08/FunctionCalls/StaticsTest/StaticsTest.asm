//['function', 'Sys.init', '0']
(Sys.init)
@SP
D=M
@R13
M=D
@0
D=A
@loop-1
D;JEQ
(loop1)
@SP
M=M+1
D=M
A=M-1
M=0
@0
D=D-A
@R13
D=D-M
@loop1
D;JLT
(loop-1)
//['push', 'constant', '6']
@6
D=A
@SP
M=M+1
A=M-1
M=D
//['push', 'constant', '8']
@8
D=A
@SP
M=M+1
A=M-1
M=D
//['call', 'Class1.set', '2']
@return4
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(return4)
//['pop', 'temp', '0']
@SP
M=M-1
A=M
D=M
@R5
M=D
//['push', 'constant', '23']
@23
D=A
@SP
M=M+1
A=M-1
M=D
//['push', 'constant', '15']
@15
D=A
@SP
M=M+1
A=M-1
M=D
//['call', 'Class2.set', '2']
@return8
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(return8)
//['pop', 'temp', '0']
@SP
M=M-1
A=M
D=M
@R5
M=D
//['call', 'Class1.get', '0']
@return10
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(return10)
//['call', 'Class2.get', '0']
@return11
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(return11)
//['label', 'END']
(Sys$END)
//['goto', 'END']
@Sys$END
0;JMP
//['function', 'Class1.set', '0']
(Class1.set)
@SP
D=M
@R13
M=D
@0
D=A
@loop-15
D;JEQ
(loop15)
@SP
M=M+1
D=M
A=M-1
M=0
@0
D=D-A
@R13
D=D-M
@loop15
D;JLT
(loop-15)
//['push', 'argument', '0']
@ARG
D=M
@0
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//['pop', 'static', '0']
@SP
M=M-1
A=M
D=M
@Class1.0
M=D
//['push', 'argument', '1']
@ARG
D=M
@1
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//['pop', 'static', '1']
@SP
M=M-1
A=M
D=M
@Class1.1
M=D
//['push', 'constant', '0']
@0
D=A
@SP
M=M+1
A=M-1
M=D
//['return']
@LCL
D=M
@FRAME21
M=D
@5
A=D-A
D=M
@RET
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@FRAME21
D=M
@1
A=D-A
D=M
@THAT
M=D
@FRAME21
D=M
@2
A=D-A
D=M
@THIS
M=D
@FRAME21
D=M
@3
A=D-A
D=M
@ARG
M=D
@FRAME21
D=M
@4
A=D-A
D=M
@LCL
M=D
@RET
A=M
0;JMP
//['function', 'Class1.get', '0']
(Class1.get)
@SP
D=M
@R13
M=D
@0
D=A
@loop-22
D;JEQ
(loop22)
@SP
M=M+1
D=M
A=M-1
M=0
@0
D=D-A
@R13
D=D-M
@loop22
D;JLT
(loop-22)
//['push', 'static', '0']
@Class1.0
D=M
@SP
M=M+1
A=M-1
M=D
//['push', 'static', '1']
@Class1.1
D=M
@SP
M=M+1
A=M-1
M=D
//['sub']
@SP
A=M-1
D=M
A=A-1
D=M-D
@SP
M=M-1
A=M-1
M=D
//['return']
@LCL
D=M
@FRAME26
M=D
@5
A=D-A
D=M
@RET
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@FRAME26
D=M
@1
A=D-A
D=M
@THAT
M=D
@FRAME26
D=M
@2
A=D-A
D=M
@THIS
M=D
@FRAME26
D=M
@3
A=D-A
D=M
@ARG
M=D
@FRAME26
D=M
@4
A=D-A
D=M
@LCL
M=D
@RET
A=M
0;JMP
//['function', 'Class2.set', '0']
(Class2.set)
@SP
D=M
@R13
M=D
@0
D=A
@loop-28
D;JEQ
(loop28)
@SP
M=M+1
D=M
A=M-1
M=0
@0
D=D-A
@R13
D=D-M
@loop28
D;JLT
(loop-28)
//['push', 'argument', '0']
@ARG
D=M
@0
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//['pop', 'static', '0']
@SP
M=M-1
A=M
D=M
@Class2.0
M=D
//['push', 'argument', '1']
@ARG
D=M
@1
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//['pop', 'static', '1']
@SP
M=M-1
A=M
D=M
@Class2.1
M=D
//['push', 'constant', '0']
@0
D=A
@SP
M=M+1
A=M-1
M=D
//['return']
@LCL
D=M
@FRAME34
M=D
@5
A=D-A
D=M
@RET
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@FRAME34
D=M
@1
A=D-A
D=M
@THAT
M=D
@FRAME34
D=M
@2
A=D-A
D=M
@THIS
M=D
@FRAME34
D=M
@3
A=D-A
D=M
@ARG
M=D
@FRAME34
D=M
@4
A=D-A
D=M
@LCL
M=D
@RET
A=M
0;JMP
//['function', 'Class2.get', '0']
(Class2.get)
@SP
D=M
@R13
M=D
@0
D=A
@loop-35
D;JEQ
(loop35)
@SP
M=M+1
D=M
A=M-1
M=0
@0
D=D-A
@R13
D=D-M
@loop35
D;JLT
(loop-35)
//['push', 'static', '0']
@Class2.0
D=M
@SP
M=M+1
A=M-1
M=D
//['push', 'static', '1']
@Class2.1
D=M
@SP
M=M+1
A=M-1
M=D
//['sub']
@SP
A=M-1
D=M
A=A-1
D=M-D
@SP
M=M-1
A=M-1
M=D
//['return']
@LCL
D=M
@FRAME39
M=D
@5
A=D-A
D=M
@RET
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@FRAME39
D=M
@1
A=D-A
D=M
@THAT
M=D
@FRAME39
D=M
@2
A=D-A
D=M
@THIS
M=D
@FRAME39
D=M
@3
A=D-A
D=M
@ARG
M=D
@FRAME39
D=M
@4
A=D-A
D=M
@LCL
M=D
@RET
A=M
0;JMP
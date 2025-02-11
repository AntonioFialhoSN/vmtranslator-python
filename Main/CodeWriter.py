class CodeWriter:
    def __init__(self, fname):
        self.output = []
        self.module_name = "Main"
        self.label_count = 0
        self.output_file_name = fname
        self.call_count = 0

    def set_file_name(self, s):
        self.module_name = s[:s.index(".")]
        self.module_name = self.module_name[s.rfind("/") + 1:]
        print(self.module_name)

    def register_name(self, segment, index):
        if segment == "local":
            return "LCL"
        if segment == "argument":
            return "ARG"
        if segment == "this":
            return "THIS"
        if segment == "that":
            return "THAT"
        if segment == "pointer":
            return f"R{3 + index}"
        if segment == "temp":
            return f"R{5 + index}"
        return f"{self.module_name}.{index}"

    def write_init(self):
        self.write("@256")
        self.write("D=A")
        self.write("@SP")
        self.write("M=D")
        self.write_call("Sys.init", 0)

    def write_push(self, seg, index):
        if seg == "constant":
            self.write(f"@{index} // push {seg} {index}")
            self.write("D=A")
            self.write("@SP")
            self.write("A=M")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M+1")
        elif seg in ["static", "temp", "pointer"]:
            self.write(f"@{self.register_name(seg, index)} // push {seg} {index}")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M+1")
        else:
            self.write(f"@{self.register_name(seg, 0)} // push {seg} {index}")
            self.write("D=M")
            self.write(f"@{index}")
            self.write("A=D+A")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M+1")

    def write_pop(self, seg, index):
        if seg in ["static", "temp", "pointer"]:
            self.write(f"@SP // pop {seg} {index}")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write(f"@{self.register_name(seg, index)}")
            self.write("M=D")
        else:
            self.write(f"@{self.register_name(seg, 0)} // pop {seg} {index}")
            self.write("D=M")
            self.write(f"@{index}")
            self.write("D=D+A")
            self.write("@R13")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write("@R13")
            self.write("A=M")
            self.write("M=D")

    def write_arithmetic_add(self):
        self.write("@SP // add")
        self.write("M=M-1")
        self.write("A=M")
        self.write("D=M")
        self.write("A=A-1")
        self.write("M=D+M")

    def write_arithmetic_sub(self):
        self.write("@SP // sub")
        self.write("M=M-1")
        self.write("A=M")
        self.write("D=M")
        self.write("A=A-1")
        self.write("M=M-D")

    def write_arithmetic_neg(self):
        self.write("@SP // neg")
        self.write("A=M")
        self.write("A=A-1")
        self.write("M=-M")

    def write_arithmetic_and(self):
        self.write("@SP // and")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("A=A-1")
        self.write("M=D&M")

    def write_arithmetic_or(self):
        self.write("@SP // or")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("A=A-1")
        self.write("M=D|M")

    def write_arithmetic_not(self):
        self.write("@SP // not")
        self.write("A=M")
        self.write("A=A-1")
        self.write("M=!M")

    def write_arithmetic_eq(self):
        label = f"JEQ_{self.module_name}_{self.label_count}"
        self.write("@SP // eq")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M-D")
        self.write(f"@{label}")
        self.write("D;JEQ")
        self.write("D=1")
        self.write(f"({label})")
        self.write("D=D-1")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")
        self.label_count += 1

    def write_arithmetic_gt(self):
        label_true = f"JGT_TRUE_{self.module_name}_{self.label_count}"
        label_false = f"JGT_FALSE_{self.module_name}_{self.label_count}"
        self.write("@SP // gt")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M-D")
        self.write(f"@{label_true}")
        self.write("D;JGT")
        self.write("D=0")
        self.write(f"@{label_false}")
        self.write("0;JMP")
        self.write(f"({label_true})")
        self.write("D=-1")
        self.write(f"({label_false})")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")
        self.label_count += 1

    def write_arithmetic_lt(self):
        label_true = f"JLT_TRUE_{self.module_name}_{self.label_count}"
        label_false = f"JLT_FALSE_{self.module_name}_{self.label_count}"
        self.write("@SP // lt")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M-D")
        self.write(f"@{label_true}")
        self.write("D;JLT")
        self.write("D=0")
        self.write(f"@{label_false}")
        self.write("0;JMP")
        self.write(f"({label_true})")
        self.write("D=-1")
        self.write(f"({label_false})")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")
        self.label_count += 1

    def  write_frame_push(self, value):
        self.write(f"@{value}")
        self.write("D=M")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")
    

    def  write_label(self, label):
        self.write(f"({label})")

    def  write_goto(self, label):
        self.write(f"@{label}")
        self.write("0;JMP")
    
    def write_if(self, label):
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("M=0")
        self.write(f"@{label}")
        self.write("D;JNE")
    
    
    def write_function(self, func_name, nLocals):
    
        loopLabel = f"{func_name}_INIT_LOCALS_LOOP"
        loopEndLabel = f"{func_name}_INIT_LOCALS_END"
    
        self.write(f"({func_name})// initializa local variables")
        self.write(f"@{nLocals}")
        self.write("D=A")
        self.write("@R13") # temp
        self.write("M=D")
        self.write(f"({loopLabel})")
        self.write(f"@{loopEndLabel}")
        self.write("D;JEQ")
        self.write("@0")
        self.write("D=A")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")
        self.write("@R13")
        self.write("MD=M-1")
        self.write(f"@{loopLabel}")
        self.write("0;JMP")
        self.write(f"({loopEndLabel})")

    
    def write_call(self, func_name, num_args):
        comment = f"// call {func_name} {num_args}"

        #    push return-address     // (using the label declared below)
        #    push LCL                // save LCL of the calling function
        #    push ARG                // save ARG of the calling function
        #    push THIS               // save THIS of the calling function
        #    push THAT               // save THAT of the calling function
        #    ARG = SP-n-5            // reposition ARG (n = number of args)
        #    LCL = SP                // reposiiton LCL
        #    goto f                  // transfer control
        #    (return-address)        // declare a label for the return-address
    
        return_addr = f"{func_name}_RETURN_{self.call_count}"

        self.call_count += 1

        self.write(f"@{return_addr} {comment}")  # push return-addr
        self.write("D=A")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")
    
        self.write_frame_push("LCL")
        self.write_frame_push("ARG")
        self.write_frame_push("THIS")
        self.write_frame_push("THAT")
    
        self.write(f"@{num_args}") # ARG = SP-n-5
        self.write("D=A")
        self.write("@5")
        self.write("D=D+A")
        self.write("@SP")
        self.write("D=M-D")
        self.write("@ARG")
        self.write("M=D")
    
        self.write("@SP") ; # LCL = SP
        self.write("D=M")
        self.write("@LCL")
        self.write("M=D")
    
        self.write_goto(func_name)
    
        self.write(f"({return_addr})") # (return-address)

    def  write_return(self):

        # FRAME = LCL         // FRAME is a temporary var
        # RET = *(FRAME-5)    // put the return-address in a temporary var
        # *ARG = pop()        // reposition the return value for the caller
        # SP = ARG + 1        // restore SP of the caller
        # THAT = *(FRAME - 1) // restore THAT of the caller
        # THIS = *(FRAME - 2) // restore THIS of the caller
        # ARG = *(FRAME - 3)  // restore ARG of the caller
        # LCL = *(FRAME - 4)  // restore LCL of the caller
        # goto RET            // goto return-address (in the caller's code)

    
        self.write("@LCL") # FRAME = LCL
        self.write("D=M")
    
        self.write("@R13") # R13 -> FRAME
        self.write("M=D")
    
        self.write("@5") # RET = *(FRAME-5)
        self.write("A=D-A")
        self.write("D=M")
        self.write("@R14") # R14 -> RET
        self.write("M=D")
    
        self.write("@SP") # *ARG = pop()
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@ARG")
        self.write("A=M")
        self.write("M=D")
    
        self.write("D=A") # SP = ARG+1
        self.write("@SP")
        self.write("M=D+1")
    
        self.write("@R13") # THAT = *(FRAME-1)
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@THAT")
        self.write("M=D")
    
        self.write("@R13") # THIS = *(FRAME-2)
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@THIS")
        self.write("M=D")
    
        self.write("@R13") # ARG = *(FRAME-3)
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@ARG")
        self.write("M=D")
    
        self.write("@R13") # LCL = *(FRAME-4)
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@LCL")
        self.write("M=D")
    
        self.write("@R14") # goto RET
        self.write("A=M")
        self.write("0;JMP")

    def write(self, s):
        self.output.append(f"{s}\n")

    def code_output(self):
        return "".join(self.output)

    def close(self): 

        try:
            with open(self.output_file_name, "w") as output_stream:
                output_stream.write(self.code_output())
        except IOError as e:
            print(f"Error writing to file: {e}")
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
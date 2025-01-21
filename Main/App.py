from CodeWriter import *
from Command import *
from Parser import *


def main():
    input = """
    // This file is part of www.nand2tetris.org
    // and the book "The Elements of Computing Systems"
    // by Nisan and Schocken, MIT Press.
    // File name: projects/07/MemoryAccess/BasicTest/BasicTest.vm

    // Executes pop and push commands using the virtual memory segments.
    push constant 10
    pop local 0
    push constant 21
    push constant 22
    pop argument 2
    pop argument 1
    push constant 36
    pop this 6
    push constant 42
    push constant 45
    pop that 5
    pop that 2
    push constant 510
    pop temp 6
    push local 0
    push that 5
    add
    push argument 1
    sub
    push this 6
    push this 6
    add
    sub
    push temp 6
    add
    """
    input = "push argument 3"

    code = CodeWriter()
    parser = Parser(input)
    while parser.has_more_commands():
        command = parser.next_command()
        if command.type == "ADD":
            code.write_arithmetic_add()
        elif command.type == "SUB":
            code.write_arithmetic_sub()
        elif command.type == "PUSH":
            code.write_push(command.args[0], int(command.args[1]))
        elif command.type == "POP":
            code.write_pop(command.args[0], int(command.args[1]))
        else:
            print(f"{command.type} not implemented")

    print(code.code_output())

if __name__ == "__main__":
    main()

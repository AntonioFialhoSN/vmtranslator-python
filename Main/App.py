import os
import sys
from CodeWriter import *
from Parser import Parser
from pathlib import Path

class App:

    @staticmethod
    def from_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except IOError as e:
            print(f"Error na leitura {file_path}: {e}")
            return ""

    @staticmethod
    def translate_file(file_path, code):
        input_data = App.from_file(file_path)
        parser = Parser(input_data)
        while parser.has_more_commands():
            command = parser.next_command()
            match command.type:
                case "ADD":
                    code.write_arithmetic_add()
                case "SUB":
                    code.write_arithmetic_sub()
                case "NEG":
                    code.write_arithmetic_neg()
                case "NOT":
                    code.write_arithmetic_not()
                case "EQ":
                    code.write_arithmetic_eq()
                case "LT":
                    code.write_arithmetic_lt()
                case "GT":
                    code.write_arithmetic_gt()
                case "AND":
                    code.write_arithmetic_and()
                case "OR":
                    code.write_arithmetic_or()
                case "PUSH":
                    code.write_push(command.args[0], int(command.args[1]))
                case "POP":
                    code.write_pop(command.args[0], int(command.args[1]))
                case "GOTO":
                    code.write_goto(command.args[0])                
                case "IF":
                    code.write_if(command.args[0])
                case "LABEL":
                    code.write_label(command.args[0])                    
                case "RETURN":
                    code.write_return()
                case "CALL":
                    code.write_call(command.args[0], int(command.args[1]))
                case "FUNCTION":
                    code.write_function(command.args[0], int(command.args[1]))
                case _:
                    print(f"{command.type} não implementado")

    @staticmethod
    def main(args):
        if len(args) != 2:
            print("Forneça um único argumento de caminho de arquivo.", file=sys.stderr)
            sys.exit(1)

        file_path = Path(args[1])

        if not file_path.exists():
            print("O arquivo não existe.", file=sys.stderr)
            sys.exit(1)

        if file_path.is_dir():
            output_file_name = file_path / f"{file_path.name}.asm"
            print(output_file_name)
            code = CodeWriter(output_file_name)

            code.write_init()

            for f in file_path.iterdir():
                if f.is_file() and f.suffix == ".vm":
                    print(f"Compiling {f}")
                    App.translate_file(f, code)
                    
            code.close()
        elif file_path.is_file():
            if file_path.suffix != ".vm":
                print("Forneça um nome de arquivo que termine com .vm", file=sys.stderr)
                sys.exit(1)

            input_file_name = str(file_path)
            output_file_name = input_file_name.replace(".vm", ".asm")
            code = CodeWriter(output_file_name)

            print(f"Compiling {input_file_name}")
            code.write_init()
            App.translate_file(file_path, code)

            code.close()

if __name__ == "__main__":
    App.main(sys.argv)

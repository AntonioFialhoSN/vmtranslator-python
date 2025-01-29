import os
import sys
from pathlib import Path

class App:
    @staticmethod
    def from_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
    
    @staticmethod
    def main(args):
        if len(args) != 2:
            print("Forneça um único argumento de caminho de arquivo.", file=sys.stderr)
            sys.exit(1)

        file_path = Path(args[1])

        if not file_path.exists():
            print("O arquivo não existe.", file=sys.stderr)
            sys.exit(1)


        if file_path.is_file():
            if file_path.suffix != ".vm":
                print("Forneça um nome de arquivo que termine com .vm", file=sys.stderr)
                sys.exit(1)

            input_file_name = str(file_path)
            print(input_file_name)
            output_file_name = input_file_name.replace(".vm", ".asm")
            print(output_file_name)

if __name__ == "__main__":
    App.main(sys.argv)

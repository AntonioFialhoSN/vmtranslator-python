from Command import *

class Parser:

    def __init__(self, input_data):
        # Quebra a entrada em linhas
        lines = input_data.splitlines()
        
        # Processa as linhas: remove espaços em branco, ignora linhas de comentário e vazias
        self.commands = [
            line.split()  # Divide cada linha em palavras
            for line in lines
            if line.strip() and not line.strip().startswith("//")
        ]

    def has_more_commands(self):
        return len(self.commands) > 0

    def next_command(self):
        return Command(self.commands.pop(0))
    

''' 
#desenvolvimento teste
input_data = """push constant 10
pop local 0
push constant 21"""
parser = Parser(input_data)

while parser.has_more_commands():
    command = parser.next_command()
    print(command.type, command.args)
'''
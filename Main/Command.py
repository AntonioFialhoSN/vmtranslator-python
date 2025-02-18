class Command:
    class Type:
        ADD = "ADD"
        SUB = "SUB"
        NEG = "NEG"
        EQ = "EQ"
        GT = "GT"
        LT = "LT"
        AND = "AND"
        OR = "OR"
        NOT = "NOT"
        PUSH = "PUSH"
        POP = "POP"
        LABEL = "LABEL"
        GOTO = "GOTO"
        IF = "IF"
        RETURN = "RETURN"
        CALL = "CALL"
        FUNCTION = "FUNCTION"

    def __init__(self, command):
        if command[0] == "if-goto":
            self.type = Command.Type.IF
        else:
            self.type = getattr(Command.Type, command[0].upper(), None)

        self.args = []
        for arg in command[1:]:
            pos = arg.find("//")
            if pos != -1:
                arg = arg[:pos]
            self.args.append(arg.strip())
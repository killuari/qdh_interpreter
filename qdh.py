import sys

class QDHInterpreter:
    def __init__(self):
        self.code = self.readfile()
        self.pc = 0

    def readfile(self):
        with open(sys.argv[1], 'r') as f:
            return f.read()

    def run(self):
        lines = self.code.split('\n')
        while self.pc < len(lines):
            line = lines[self.pc]
            self.pc += 1
            print(line)


interpreter = QDHInterpreter()
interpreter.run()
    
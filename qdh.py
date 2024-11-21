import sys

class QDHInterpreter:
    def __init__(self):
        self.code = self.readfile()
        self.vars = {}
        self.pc = 0

    def readfile(self):
        with open(sys.argv[1], 'r') as f:
            return f.read()

    def run(self):
        lines = self.code.split('\n')
        while self.pc < len(lines):
            line = lines[self.pc]
            
            if "=" in line:
                var, expr = line.split("=")
                vars[var] = expr
            
            self.pc += 1

    def tokenize(self, expr):
        tokens = expr.split()
        return tokens

    def eval_postfix(self, postfix):
        pass

    def infix_to_postfix(self, tokens):
        precedence = {'+':1, '-':1, '*':2, '/':2, '^':3}
        postfix = []
        operators = []
        for token in tokens:
            if token.isdigit():
                postfix.append(token)
            elif token in precedence:
                while operators and operators[-1] != '(' and precedence[token] <= precedence[operators[-1]]:
                    postfix.append(operators.pop())
                else:
                    operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators[-1] != '(':
                    postfix.append(operators.pop())
                operators.pop()
        while operators:
            postfix.append(operators.pop())
        return postfix

    def test(self):
        expr = "1 + 2 * 3 - 4 * 5"
        tokens = self.tokenize(expr)
        postfix = self.infix_to_postfix(tokens)
        print(postfix)

interpreter = QDHInterpreter()
interpreter.test()
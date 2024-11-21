import sys, re

#file = sys.argv[1]
file = "test.qdh"

class QDHInterpreter:
    def __init__(self):
        self.code = self.readfile()
        self.vars = {}
        self.stack = []
        self.pc = 0

    def readfile(self):
        with open(file, 'r') as f:
            return f.read()

    def run(self):
        lines = self.code.split('\n')
        while self.pc < len(lines):
            line = lines[self.pc]
            if "=" in line:
                var, expr = line.split(" = ")
                tokens = self.tokenize(expr)
                postfix = self.infix_to_postfix(tokens)
                self.vars[var] = self.eval_postfix(postfix)
            elif line.startswith("print"):
                if line[6] == '"':
                    print(line[7:-2])
                else:
                    tokens = self.tokenize(line[6:-1])
                    postfix = self.infix_to_postfix(tokens)
                    print(self.eval_postfix(postfix))
            self.pc += 1

    def tokenize(self, expr):
        token_pattern = r'[a-zA-Z_][a-zA-Z_0-9]*|\d+|[+\-*/()^]'
        return re.findall(token_pattern, expr)

    def infix_to_postfix(self, tokens):
        precedence = {'+':1, '-':1, '*':2, '/':2, '^':3}
        postfix = []
        operators = []
        for token in tokens:
            if token.isdigit():
                postfix.append(token)
            elif token in self.vars:
                postfix.append(self.vars[token])
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

    def eval_postfix(self, postfix):
        for token in postfix:
            if isinstance(token, int) or isinstance(token, float):
                self.stack.append(token)
            elif token.isdigit():
                self.stack.append(int(token))
            else:
                right = self.stack.pop()
                left = self.stack.pop()
                if token == '+':
                    self.stack.append(left + right)
                elif token == '-':
                    self.stack.append(left - right)
                elif token == '*':
                    self.stack.append(left * right)
                elif token == '/':
                    self.stack.append(left / right)
                elif token == '^':
                    self.stack.append(left ** right)
        return self.stack.pop()

interpreter = QDHInterpreter()
interpreter.run()
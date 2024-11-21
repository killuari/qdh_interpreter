#!/usr/bin/env python

import sys, re

#file = sys.argv[1]
file = "test.qdh"

class QDHInterpreter:
    def __init__(self):
        self.code = self.readfile()
        self.lines = self.code.split('\n')
        self.vars = {}
        self.stack = []
        self.pc = 0

    def readfile(self):
        try:
            with open(file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f"File {file} not found")
            sys.exit(1)

    def set_pc_to_end(self):
        left = 1
        while left > 0:
            self.pc += 1
            line = self.lines[self.pc].lstrip()
            if "{" in line or "}" in line:
                for char in line:
                    if char == "}":
                        left -= 1
                    elif char == "{":
                        left += 1
        return line

    def set_pc_to_start(self):
        left = 1
        while left > 0:
            self.pc -= 1
            line = self.lines[self.pc].lstrip()
            if "{" in line or "}" in line:
                for char in line:
                    if char == "}":
                        left += 1
                    elif char == "{":
                        left -= 1
        return line

    def run(self):
        while self.pc < len(self.lines):
            line = self.lines[self.pc].lstrip()
            if line.startswith("//"):
                self.pc += 1
            elif line.startswith("if"):
                if self.eval_expr(line[3:-1]) == "true":
                    self.pc += 1
                else:
                    line = self.set_pc_to_end()
                    self.pc += 1
                    
            elif line.startswith("while"):
                if self.eval_expr(line[5:-1]) == "true":
                    self.pc += 1
                else:
                    line = self.set_pc_to_end()
                    self.pc += 1

            elif line.startswith("}"):
                start = self.pc
                line = self.set_pc_to_start()
                if line.startswith("if"):
                    self.pc = start + 1
                if line.startswith("while"):
                    if self.eval_expr(line[5:-1]) == "true":
                        self.pc += 1
                    else:
                        self.pc = start + 1

            elif line.startswith("println"):
                print(self.eval_expr(line[8:-1]))
                self.pc += 1

            elif line.startswith("print"):
                print(self.eval_expr(line[6:-1]), end="")
                self.pc += 1

            elif "=" in line:
                var, expr = line.split("=", maxsplit=1)
                var = var.rstrip()
                self.vars[var] = self.eval_expr(expr)
                self.pc += 1

            else:
                self.pc += 1

    def eval_expr(self, expr):
        expr = expr.lstrip()
        if expr.startswith('"'):
            evaluation = ""
            string = expr[1:-1]
            idx = 0
            while idx < len(string):
                char = string[idx]
                if char == "\\" and string[idx + 1] == "{":
                    ex_start = idx + 2
                    ex_end = string.find("}", ex_start)
                    evaluation += str(self.eval_expr(string[ex_start:ex_end]))
                    idx = ex_end + 1
                else:
                    evaluation += char
                    idx += 1
        else:
            tokens = self.tokenize(expr)
            postfix = self.infix_to_postfix(tokens)
            evaluation = self.eval_postfix(postfix)
        return evaluation

    def tokenize(self, expr):
        token_pattern = r'[a-zA-Z_][a-zA-Z_0-9]*|\d+|true|false|[+\-*/<>=!()^]+'
        return re.findall(token_pattern, expr)

    def infix_to_postfix(self, tokens):
        precedence = {'<=':1, '<':1, '>=':1, '>':1, '==':1, '+':1, '-':1, '*':2, '/':2, '^':3}
        postfix = []
        operators = []
        for token in tokens:
            if token.isdigit() or token in ['true', 'false']:
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
            if isinstance(token, int) or isinstance(token, float) or token in ['true', 'false']:
                self.stack.append(token)
            elif token.isdigit():
                self.stack.append(int(token))
            elif token in self.vars:
                self.stack.append(self.vars[token])
            elif token in "+-*/^":
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
            elif token in ['<=', '<', '>=', '>', '==']:
                right = self.stack.pop()
                left = self.stack.pop()
                if token == '<=':
                    self.stack.append(str(left <= right).lower())
                elif token == '<':
                    self.stack.append(str(left < right).lower())
                elif token == '>=':
                    self.stack.append(str(left >= right).lower())
                elif token == '>':
                    self.stack.append(str(left > right).lower())
                elif token == '==':
                    self.stack.append(str(left == right).lower())
        return self.stack.pop()

interpreter = QDHInterpreter()
interpreter.run()
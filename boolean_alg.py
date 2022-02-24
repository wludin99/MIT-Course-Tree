import re


##classes to deal with symbolic boolean algebra expressions

class Symbol:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(other, self)

class Var(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Var(' + repr(self.name) + ')'

    def simplify(self):
        return Var(self.name)

    def eval(self, mapping):
        return mapping[self.name]

    def flatten(self):
        return self.name

class Op(Symbol):
    def __init__(self, clauses):
        '''vars is list of items in and/or operator'''
        self.clauses = clauses

    def __repr__(self):
        s = self.operation + '(['
        for i in range(len(self.clauses)):
            s += self.clauses[i].__repr__()
            if i != len(self.clauses) - 1:
                s += ','
        s +=  '])'
        return s

    def __str__(self):
        s = '('
        for i in range(len(self.clauses)):
            s += self.clauses[i].__str__()
            if i != len(self.clauses) - 1:
                s += self.operand
        s += ')'
        return s

    def flatten(self):
        if len(L) == 1:
            if type(L[0]) == list:
                result = flatten(L[0])
            else:
                result = L
        elif type(L[0]) == list:
            result = flatten(L[0]) + flatten(L[1:])
        else:
            result = [L[0]] + flatten(L[1:])
        return result



class And(Op):
    def __init__(self, clauses):
        super().__init__(clauses)
        self.operation = 'And'
        self.operand = ' & '

    def eval(self, mapping):
        return all([clause.eval(mapping) for clause in self.clauses])

class Or(Op):
    def __init__(self, clauses):
        super().__init__(clauses)
        self.operation = 'Or'
        self.operand = ' | '

    def eval(self, mapping):
        return any([clause.eval(mapping) for clause in self.clauses])

def tokenize(req):
    if req == None:
        return
    req = req.replace('(GIR)', '')
    l = re.split(r"( and | or |\(|\)|,)", req)
    tokens = []
    for token in l:
        token = token.strip(' .;,')
        token = token.lower().replace(' ', '')
        if token == '':
            pass
        else:
            tokens.append(token)
    return tokens

def parse(expr):
    if expr == None or expr == ['none']:
        return None
    def listize(index):
        if index == len(expr) or expr[index] == ')':
            return ([], index)
        elif expr[index] == '(':
            subexpr, next_index = listize(index+1)
            return ([subexpr] + listize(next_index+1)[0],listize(next_index+1)[1])
        else:
            next_expression, next_index = listize(index+1)
            return ([expr[index]] + next_expression, next_index)
    nested_expression, length = listize(0)
    def parse_expression(nested_expression):
        if isinstance(nested_expression, str):
            return Var(nested_expression)
        if len(nested_expression) == 1:
            return Var(nested_expression[0])
        if 'and' in nested_expression:
            nested_expression.remove('and')
            return And([parse_expression(el) for el in nested_expression])
        if 'or' in nested_expression:
            nested_expression.remove('or')
            return Or([parse_expression(el) for el in nested_expression])
    return parse_expression(nested_expression)


def sym(expr):
    return parse(tokenize(expr))

if __name__ == "__main__":
    expr = ['(', '18.06', '18.700', 'or', '18.701', ')', 'and', '(', '18.100a', '18.100b', '18.100p', 'or', '18.100q', ')']
    print(parse(expr))

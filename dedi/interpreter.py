import operator
from parser import make_tree


class Interpreter():
    def __init__(self):
        self.funcs = {
            '+': operator.add,
            '*': operator.mul,
            'pr': self.pr,
            'sum': self.list_sum,
            'l': self.l,
            'h': operator.itemgetter(0),
            'la': self.la,
            'lu': self.lu
        }
        self.defined_funcs = {
        }
        self.variables = {
        }
        self.level = 0

    def parse_params(self, param_tokens):
        return [param_token[1] for param_token in param_tokens]

    def get_var(self, varname, params={}):
        if params.get(varname, False):
            value = params.get(varname)
        elif self.variables.get(varname, False):
            value = self.variables.get(varname)[0]
        else:
            sys.stderr.write('Variable '
                             + varname
                             + ' is not defined in parameters or variables')
            raise ValueError()
        return value

    def fill_params(self, tree, params):
        callparams = []
        for token in tree[1:]:
        #    import pprint
        #    pprint.pprint(token)
            if token[1] == 'FUNC':
                callparams.append(self.interpret(token[0], params))
            elif token[1] == 'NUM':
                callparams.append(token[0])
            elif token[1] == 'STR':
                callparams.append(token[0][1:-1])
            elif token[1] == 'IDEN':
                callparams.append(self.get_var(token[0][0], params))
                #print 'func: ' + str(tree[0])
                #print 'params: ' + str(params)
        return callparams

    def interpret(self, tree, params):
        # TODO Garbage?
        #print tree
        if tree[1] == 'FUNC':
            result = self.interpret(tree[0], {})
            return result
        if self.defined_funcs.get(tree[0][0], False):
            func = self.defined_funcs.get(tree[0][0])
            params = {}
            for param_name, value in zip(func[0], tree[1:len(func[0])+1]):
                params[param_name] = value
            return self.interpret(func[1], params)
        elif tree[0][0] == 'sb':
            result = None
            for func in tree[1:]:
                result = self.interpret(func, {})
            return result
        elif tree[0][0] == 'fn':
            func = [self.parse_params(tree[2][0]), tree[3]]
            self.defined_funcs[tree[1][0]] = func
            return
        elif tree[0][0] == 'var':
            value = None
            if tree[2][1] == 'FUNC':
                value = self.interpret(tree[2][0], params)
            elif tree[2][1] == 'STR' or tree[2][1] == 'NUM':
                value = tree[2][0]
            self.variables[tree[1][0]] = [value, self.level-1]
            return
        callparams = self.fill_params(tree, {})
        return self.funcs.get(tree[0][0])(*callparams)

    def add(self, a, b):
        return a + b

    def mul(self, a, b):
        return a * b

    def pr(self, a):
        print(a)

    def list_sum(self, l):
        return reduce(operator.add, l)

    def l(self, *args):
        return list(args)

    def lu(self, *args):
        result = []
        for i in args:
            result += i
        return result

    def la(self, l, *args):
        return l + list(args)


def interpret(text):
    tree = make_tree(text)
    #from pprint import pprint
    #pprint(tree)
    interpreter = Interpreter()
    for layer1_func in tree:
        interpreter.interpret(layer1_func, {})


def interpret_file(filename):
    #print sys.argv
    f = open(filename, 'r')
    text = f.read()
    f.close()
    interpret(text)


def test():
    interpret('(pr (+ 5 (+ 2 4)))')
    interpret('(pr "asdasdsa")')
    interpret('(pr (+ "asdasda" "asdasdsa"))')
    interpret('(pr (sum (l 2 3 4)))')
    interpret('(pr (h (la (l 2 3) 1)))')
    interpret('(la (l 1 2) (l 2 3))')
    interpret('(sb (pr "111") (pr "asdas"))')
    interpret('(sb (var a 1) (pr (l a 1 2)))')
    interpret('(sb (var a (l 1 2 3 4)) (pr (lu a (l 1 2))))')
    interpret('(fn cust_list (a b) (l 1 2))')
    interpret('(sb (fn cust_list (a b) (l 1 2)) (pr(cust_list 1 2)))')

import sys
if __name__ == "__main__":
    interpret_file(sys.argv[1])

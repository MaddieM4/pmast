import pmast
from ast import *

source = '''
def some_function(a, b):
    a - 3
    return a + b
'''
tree = parse(source)

pm = pmast.PatternDispatch()

@pm('BinOp.Add')
def add(data, node_binop, node_add):
    assert node_add is node_binop.op
    assert isinstance(node_add, Add)
    data['addleft'] = node_binop.left

@pm('BinOp.Sub')
def sub(data, node_binop, node_sub):
    data['subright'] = node_binop.right

def test_dispatch():
    data = pm.dispatch(tree)
    assert isinstance(data['addleft'], Name)
    assert data['addleft'].id == 'a'
    assert data['subright'].n == 3

def test_dispatch_on_function():
    def example_func():
        return 8 + 9 - 10
    data = pm.dispatch(example_func)
    assert data['addleft'].n == 8
    assert data['subright'].n == 10

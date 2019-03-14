import ast
import inspect
from collections import namedtuple

def ast_type(text):
    if text == '*':
        return ast.AST
    if isinstance(text, type):
        return text # Already translated
    if not hasattr(ast, text):
        raise TypeError('No AST node type ' + text)
    got = getattr(ast, text)
    if not issubclass(got, ast.AST):
        raise TypeError('No AST node type ' + text)
    return got

_nt = namedtuple('Pattern', 't constraints child')
class Pattern(_nt):
    __slots__ = ()
    def __new__(cls, name='*', child=None, **constraints):
        return super().__new__(cls,
            ast_type(name),
            tuple(constraints.items()),
            child,
        )
    
    @classmethod
    def from_spec(cls, text):
        # TODO: understand constraints
        segments = text.split('.')
        segments.reverse()
        pattern = None
        for s in segments:
            pattern = Pattern(s, pattern)
        return pattern

    def match(self, node):
        # TODO: respect constraints
        if not isinstance(node, self.t):
            return None

        # Okay, we're a match so far. Check children.
        if not self.child:
            return (node,)
        for cnode in ast.iter_child_nodes(node):
            found = self.child.match(cnode)
            if found:
                return (node, *found)
        return None

def parse(tree):
    if isinstance(tree, ast.AST):
        return tree
    elif isinstance(tree, str):
        return ast.parse(tree)
    else:
        source = inspect.getsource(tree)
        fixed = inspect.cleandoc("  \n" + source) # Normalize indents a bit
        return ast.parse(fixed)

class PatternDispatch(object):
    def __init__(self):
        self.patterns = []

    def __call__(self, spec):
        def outer(inner):
            pat = Pattern.from_spec(spec)
            self.patterns.append((pat, inner))
        return outer

    def dispatch(self, tree, data=None):
        if data is None:
            data = dict()

        for node in ast.walk(parse(tree)):
            for (pattern, callback) in self.patterns:
                match = pattern.match(node)
                if match:
                    callback(data, *match)
        return data

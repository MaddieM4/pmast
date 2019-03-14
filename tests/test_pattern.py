import pytest
from pmast import ast_type, Pattern
from ast import *

@pytest.mark.parametrize('text,t', [
    ('FunctionDef', FunctionDef),
    ('Sub', Sub),
    ('DoesNotExistAtAll', None),
    ('copy_location', None), # Actually a function
    ('*', AST),
])
def test_ast_type(text, t):
    if t is None:
        with pytest.raises(TypeError):
            ast_type(text)
    else:
        assert ast_type(text) == t

@pytest.mark.parametrize('text,pattern', [
    ('FunctionDef', Pattern(FunctionDef) ),
    ('BinOp.Add', Pattern(BinOp, child=Pattern(Add)) ),
    ('Expr.BinOp.Add', Pattern(Expr, child=Pattern(BinOp, child=Pattern(Add))) ),
])
def test_spec_parsing(text, pattern):
    assert Pattern.from_spec(text) == pattern

@pytest.mark.parametrize('source,spec,ok', [
    ('a + 3', 'Expr', True),
    ('a + 3', 'Expr.BinOp', True),
    ('a + 3', 'Expr.BinOp.Num', True),
    ('a + 3', 'Expr.BinOp.Str', False),
    ('a + 3', 'Expr.*.Name', True),
    ('a + 3', 'Expr.*.Str', False),
])
def test_match(source, spec, ok):
    tree = parse(source).body[0]
    pattern = Pattern.from_spec(spec)
    match = pattern.match(tree)
    if ok:
        assert isinstance(match[0], Expr) # Simple sanity check before thorough iteration
        pos = 0
        while pattern:
            assert isinstance(match[pos], pattern.t)
            pos += 1
            pattern = pattern.child
    else:
        assert match is None

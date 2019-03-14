# Pattern Matcher for Python AST

This tool is about finding patterns in AST structures. As such, it may
be useful for static analysis and linting.

```python
import pmast
pm = pmast.PatternDispatch()

@pm('FunctionDef.Return')
def on_return(data, fd, ret):
    # Store return statement (an ast node) for each function
    data[fd.name] = ret

class Foo(object):
    def x(self):
        return 3

    def y(self, foo, bar):
        return 4

data = pm.dispatch(Foo)
assert data['x'].value.n == 3
assert data['y'].value.n == 4
```

The intent here is to be a little bit like XPath for the Python AST module.

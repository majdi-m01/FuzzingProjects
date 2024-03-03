constraint="""
forall <FunctionDef> def:
  exists <Return>:
    exists <integer> x:
        (inside(x, <Return>) and str.to.int(x) > 995 and str.to.int(x) < 1005)
"""

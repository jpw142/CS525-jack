import sys
sys.setrecursionlimit(10000)

############################################################
# datatype styp
############################################################

class styp:
    ctag = ""
    def __str__(self):
        return ("styp(" + self.ctag + ")")

class styp_bas(styp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "STbas"
    def __str__(self):
        return ("STbas(" + self.arg1 + ")")

class styp_xyz(styp):
    """Existential type variable with mutable ref cell for unification"""
    def __init__(self):
        self.ref = [None]  # ref(optn(styp)) — None means unresolved
        self.ctag = "STxyz"
    def __str__(self):
        if self.ref[0] is not None:
            return str(self.ref[0])
        return "STxyz(?)"

class styp_tup(styp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "STtup"
    def __str__(self):
        return ("STtup(" + str(self.arg1) + ", " + str(self.arg2) + ")")

class styp_fun(styp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "STfun"
    def __str__(self):
        return ("STfun(" + str(self.arg1) + ", " + str(self.arg2) + ")")

class styp_lazy(styp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "STlazy"
    def __str__(self):
        return ("STlazy(" + str(self.arg1) + ")")

class styp_list(styp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "STlist"
    def __str__(self):
        return ("STlist(" + str(self.arg1) + ")")

class styp_arry(styp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "STarry"
    def __str__(self):
        return ("STarry(" + str(self.arg1) + ")")

class styp_stcn(styp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "STstcn"
    def __str__(self):
        return ("STstcn(" + str(self.arg1) + ")")

# Common type constants
styp_int  = styp_bas("int")
styp_bool = styp_bas("bool")
styp_str  = styp_bas("string")
styp_unit = styp_bas("unit")

def styp_new_xyz():
    return styp_xyz()

############################################################
# Type normalization: follow STxyz chains
############################################################

def styp_norm(st):
    while st.ctag == "STxyz" and st.ref[0] is not None:
        st = st.ref[0]
    return st

############################################################
# Occurs check
############################################################

def styp_occurs(xz, st):
    """Check if xz occurs in st (for occurs check in unification)"""
    st = styp_norm(st)
    if st.ctag == "STxyz":
        return xz is st
    if st.ctag == "STbas":
        return False
    if st.ctag == "STtup":
        return styp_occurs(xz, st.arg1) or styp_occurs(xz, st.arg2)
    if st.ctag == "STfun":
        return styp_occurs(xz, st.arg1) or styp_occurs(xz, st.arg2)
    if st.ctag == "STlazy":
        return styp_occurs(xz, st.arg1)
    if st.ctag == "STlist":
        return styp_occurs(xz, st.arg1)
    if st.ctag == "STarry":
        return styp_occurs(xz, st.arg1)
    if st.ctag == "STstcn":
        return styp_occurs(xz, st.arg1)
    return False

############################################################
# Unification
############################################################

def styp_unify(st1, st2):
    st1 = styp_norm(st1)
    st2 = styp_norm(st2)
    if st1 is st2:
        return
    if st1.ctag == "STxyz":
        assert not styp_occurs(st1, st2), \
            "Occurs check failed: " + str(st1) + " in " + str(st2)
        st1.ref[0] = st2
        return
    if st2.ctag == "STxyz":
        assert not styp_occurs(st2, st1), \
            "Occurs check failed: " + str(st2) + " in " + str(st1)
        st2.ref[0] = st1
        return
    if st1.ctag == "STbas" and st2.ctag == "STbas":
        assert st1.arg1 == st2.arg1, \
            "Type mismatch: " + str(st1) + " vs " + str(st2)
        return
    if st1.ctag == "STtup" and st2.ctag == "STtup":
        styp_unify(st1.arg1, st2.arg1)
        styp_unify(st1.arg2, st2.arg2)
        return
    if st1.ctag == "STfun" and st2.ctag == "STfun":
        styp_unify(st1.arg1, st2.arg1)
        styp_unify(st1.arg2, st2.arg2)
        return
    if st1.ctag == "STlazy" and st2.ctag == "STlazy":
        styp_unify(st1.arg1, st2.arg1)
        return
    if st1.ctag == "STlist" and st2.ctag == "STlist":
        styp_unify(st1.arg1, st2.arg1)
        return
    if st1.ctag == "STarry" and st2.ctag == "STarry":
        styp_unify(st1.arg1, st2.arg1)
        return
    if st1.ctag == "STstcn" and st2.ctag == "STstcn":
        styp_unify(st1.arg1, st2.arg1)
        return
    assert False, "Type mismatch: " + str(st1) + " vs " + str(st2)

############################################################
# datatype dexp
############################################################

class dexp:
    ctag = ""

class dexp_int(dexp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "DEint"
    def __str__(self):
        return ("DEint(" + str(self.arg1) + ")")

class dexp_btf(dexp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "DEbtf"
    def __str__(self):
        return ("DEbtf(" + str(self.arg1) + ")")

class dexp_str(dexp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "DEstr"
    def __str__(self):
        return ("DEstr(" + repr(self.arg1) + ")")

class dexp_var(dexp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "DEvar"
    def __str__(self):
        return ("DEvar(" + self.arg1 + ")")

class dexp_lam(dexp):
    """DElam(dvar, body) — untyped lambda"""
    def __init__(self, arg1, arg2):
        self.arg1 = arg1  # dvar
        self.arg2 = arg2  # body
        self.ctag = "DElam"
    def __str__(self):
        return ("DElam(" + self.arg1 + ", " + str(self.arg2) + ")")

class dexp_app(dexp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1  # fun
        self.arg2 = arg2  # arg
        self.ctag = "DEapp"
    def __str__(self):
        return ("DEapp(" + str(self.arg1) + ", " + str(self.arg2) + ")")

class dexp_opr(dexp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1  # operator name
        self.arg2 = arg2  # list of dexp
        self.ctag = "DEopr"
    def __str__(self):
        return ("DEopr(" + self.arg1 + ", " + str(self.arg2) + ")")

class dexp_fst(dexp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "DEfst"
    def __str__(self):
        return ("DEfst(" + str(self.arg1) + ")")

class dexp_snd(dexp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "DEsnd"
    def __str__(self):
        return ("DEsnd(" + str(self.arg1) + ")")

class dexp_tup(dexp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "DEtup"
    def __str__(self):
        return ("DEtup(" + str(self.arg1) + ", " + str(self.arg2) + ")")

class dexp_if0(dexp):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1  # test
        self.arg2 = arg2  # then
        self.arg3 = arg3  # else
        self.ctag = "DEif0"
    def __str__(self):
        return ("DEif0(" + str(self.arg1) + ", " + str(self.arg2) + ", " + str(self.arg3) + ")")

class dexp_fix(dexp):
    """DEfix(fun_name, arg_name, body) — untyped fix"""
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1  # fun name
        self.arg2 = arg2  # arg name
        self.arg3 = arg3  # body
        self.ctag = "DEfix"
    def __str__(self):
        return ("DEfix(" + self.arg1 + ", " + self.arg2 + ", " + str(self.arg3) + ")")

class dexp_let(dexp):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1  # var name
        self.arg2 = arg2  # def
        self.arg3 = arg3  # scope
        self.ctag = "DElet"
    def __str__(self):
        return ("DElet(" + self.arg1 + ", " + str(self.arg2) + ", " + str(self.arg3) + ")")

class dexp_list_nil(dexp):
    def __init__(self):
        self.ctag = "DElist_nil"
    def __str__(self):
        return "DElist_nil()"

class dexp_list_cons(dexp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1  # head
        self.arg2 = arg2  # tail
        self.ctag = "DElist_cons"
    def __str__(self):
        return ("DElist_cons(" + str(self.arg1) + ", " + str(self.arg2) + ")")

class dexp_lazy(dexp):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "DElazy"
    def __str__(self):
        return ("DElazy(" + str(self.arg1) + ")")

class dexp_stcn_nil(dexp):
    def __init__(self):
        self.ctag = "DEstcn_nil"
    def __str__(self):
        return "DEstcn_nil()"

class dexp_stcn_cons(dexp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1  # head
        self.arg2 = arg2  # tail (lazy stream)
        self.ctag = "DEstcn_cons"
    def __str__(self):
        return ("DEstcn_cons(" + str(self.arg1) + ", " + str(self.arg2) + ")")

class dexp_arry_size_val(dexp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1  # size
        self.arg2 = arg2  # val
        self.ctag = "DEarry_size_val"
    def __str__(self):
        return ("DEarry_size_val(" + str(self.arg1) + ", " + str(self.arg2) + ")")

class dexp_arry_size_fun(dexp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1  # size
        self.arg2 = arg2  # fun (int -> a)
        self.ctag = "DEarry_size_fun"
    def __str__(self):
        return ("DEarry_size_fun(" + str(self.arg1) + ", " + str(self.arg2) + ")")

class dexp_anno(dexp):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1  # dexp
        self.arg2 = arg2  # styp annotation
        self.ctag = "DEanno"
    def __str__(self):
        return ("DEanno(" + str(self.arg1) + ", " + str(self.arg2) + ")")

class dexp_lam1(dexp):
    """DElam1(dvar, styp, body) — typed lambda"""
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1  # dvar
        self.arg2 = arg2  # styp
        self.arg3 = arg3  # body
        self.ctag = "DElam1"
    def __str__(self):
        return ("DElam1(" + self.arg1 + ", " + str(self.arg2) + ", " + str(self.arg3) + ")")

class dexp_fix1(dexp):
    """DEfix1(fun_name, arg_name, arg_type, body, res_type) — typed fix"""
    def __init__(self, arg1, arg2, arg3, arg4, arg5):
        self.arg1 = arg1  # fun name
        self.arg2 = arg2  # arg name
        self.arg3 = arg3  # arg type
        self.arg4 = arg4  # body
        self.arg5 = arg5  # result type
        self.ctag = "DEfix1"
    def __str__(self):
        return ("DEfix1(" + self.arg1 + ", " + self.arg2 + ", " + str(self.arg3) + ", " + str(self.arg4) + ", " + str(self.arg5) + ")")

############################################################
# Type context for type inference
############################################################

class tctx:
    ctag = ""

class tctx_nil(tctx):
    def __init__(self):
        self.ctag = "CXnil"

class tctx_cons(tctx):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1  # var name
        self.arg2 = arg2  # styp
        self.arg3 = arg3  # rest of context
        self.ctag = "CXcons"

def tctx_search(ctx, x00):
    if ctx.ctag == "CXnil":
        return None
    if ctx.ctag == "CXcons":
        if ctx.arg1 == x00:
            return ctx.arg2
        else:
            return tctx_search(ctx.arg3, x00)
    raise TypeError(ctx)

############################################################
# Helper: determine operator result type
############################################################

# Arithmetic operators: int * int -> int
_arith_ops = {"+", "-", "*", "/", "%"}
# Comparison operators: int * int -> bool
_cmp_ops = {"<", ">", "<=", ">=", "=", "!=", "cmp_int"}
# Boolean operators
_bool_ops = {"&&", "||"}

def _opr_tinfer(pnm, arg_types):
    """Infer the type of a primitive operation."""
    if pnm in _arith_ops:
        assert len(arg_types) == 2
        styp_unify(arg_types[0], styp_int)
        styp_unify(arg_types[1], styp_int)
        return styp_int
    if pnm in _cmp_ops or pnm == "cmp":
        assert len(arg_types) == 2
        styp_unify(arg_types[0], styp_int)
        styp_unify(arg_types[1], styp_int)
        if pnm == "cmp":
            return styp_int
        return styp_bool
    if pnm in _bool_ops:
        assert len(arg_types) == 2
        styp_unify(arg_types[0], styp_bool)
        styp_unify(arg_types[1], styp_bool)
        return styp_bool
    if pnm == "not":
        assert len(arg_types) == 1
        styp_unify(arg_types[0], styp_bool)
        return styp_bool
    if pnm == "neg":
        assert len(arg_types) == 1
        styp_unify(arg_types[0], styp_int)
        return styp_int
    if pnm == "print":
        # print can take anything, returns unit
        return styp_unit
    if pnm == "string_length":
        assert len(arg_types) == 1
        styp_unify(arg_types[0], styp_str)
        return styp_int
    if pnm == "string_append":
        assert len(arg_types) == 2
        styp_unify(arg_types[0], styp_str)
        styp_unify(arg_types[1], styp_str)
        return styp_str
    if pnm == "tostr":
        assert len(arg_types) == 1
        # converts int to string
        styp_unify(arg_types[0], styp_int)
        return styp_str
    # List operations
    if pnm == "list_length":
        assert len(arg_types) == 1
        # arg must be list(alpha)
        alpha = styp_new_xyz()
        styp_unify(arg_types[0], styp_list(alpha))
        return styp_int
    if pnm == "list_head":
        assert len(arg_types) == 1
        alpha = styp_new_xyz()
        styp_unify(arg_types[0], styp_list(alpha))
        return alpha
    if pnm == "list_tail":
        assert len(arg_types) == 1
        alpha = styp_new_xyz()
        list_a = styp_list(alpha)
        styp_unify(arg_types[0], list_a)
        return list_a
    # Array operations
    if pnm == "arry_get":
        assert len(arg_types) == 2
        alpha = styp_new_xyz()
        styp_unify(arg_types[0], styp_arry(alpha))
        styp_unify(arg_types[1], styp_int)
        return alpha
    if pnm == "arry_set":
        assert len(arg_types) == 3
        alpha = styp_new_xyz()
        styp_unify(arg_types[0], styp_arry(alpha))
        styp_unify(arg_types[1], styp_int)
        styp_unify(arg_types[2], alpha)
        return styp_unit
    if pnm == "arry_length":
        assert len(arg_types) == 1
        alpha = styp_new_xyz()
        styp_unify(arg_types[0], styp_arry(alpha))
        return styp_int
    # Stream operations
    if pnm == "stcn_head":
        assert len(arg_types) == 1
        alpha = styp_new_xyz()
        styp_unify(arg_types[0], styp_stcn(alpha))
        return alpha
    if pnm == "stcn_tail":
        assert len(arg_types) == 1
        alpha = styp_new_xyz()
        stcn_a = styp_stcn(alpha)
        styp_unify(arg_types[0], stcn_a)
        return stcn_a
    # Lazy operations
    if pnm == "lazy_force":
        assert len(arg_types) == 1
        alpha = styp_new_xyz()
        styp_unify(arg_types[0], styp_lazy(alpha))
        return alpha
    assert False, "Unknown operator: " + pnm

############################################################
# dexp_tinfer: type inference
############################################################

def dexp_tinfer(de0):
    return dexp_tinfer01(de0, tctx_nil())

def dexp_tinfer01(de0, ctx):
    if de0.ctag == "DEint":
        return styp_int
    if de0.ctag == "DEbtf":
        return styp_bool
    if de0.ctag == "DEstr":
        return styp_str
    if de0.ctag == "DEvar":
        st0 = tctx_search(ctx, de0.arg1)
        assert st0 is not None, "Unbound variable: " + de0.arg1
        return st0
    if de0.ctag == "DElam":
        # Untyped lambda: infer arg type with fresh existential
        x01 = de0.arg1
        st_arg = styp_new_xyz()
        ctx1 = tctx_cons(x01, st_arg, ctx)
        st_body = dexp_tinfer01(de0.arg2, ctx1)
        return styp_fun(st_arg, st_body)
    if de0.ctag == "DElam1":
        # Typed lambda
        x01 = de0.arg1
        st_arg = de0.arg2
        ctx1 = tctx_cons(x01, st_arg, ctx)
        st_body = dexp_tinfer01(de0.arg3, ctx1)
        return styp_fun(st_arg, st_body)
    if de0.ctag == "DEapp":
        st_fun = dexp_tinfer01(de0.arg1, ctx)
        st_arg = dexp_tinfer01(de0.arg2, ctx)
        st_res = styp_new_xyz()
        styp_unify(st_fun, styp_fun(st_arg, st_res))
        return st_res
    if de0.ctag == "DEopr":
        pnm = de0.arg1
        arg_types = [dexp_tinfer01(a, ctx) for a in de0.arg2]
        return _opr_tinfer(pnm, arg_types)
    if de0.ctag == "DEfst":
        st0 = dexp_tinfer01(de0.arg1, ctx)
        a1 = styp_new_xyz()
        a2 = styp_new_xyz()
        styp_unify(st0, styp_tup(a1, a2))
        return a1
    if de0.ctag == "DEsnd":
        st0 = dexp_tinfer01(de0.arg1, ctx)
        a1 = styp_new_xyz()
        a2 = styp_new_xyz()
        styp_unify(st0, styp_tup(a1, a2))
        return a2
    if de0.ctag == "DEtup":
        st1 = dexp_tinfer01(de0.arg1, ctx)
        st2 = dexp_tinfer01(de0.arg2, ctx)
        return styp_tup(st1, st2)
    if de0.ctag == "DEif0":
        st_test = dexp_tinfer01(de0.arg1, ctx)
        styp_unify(st_test, styp_bool)
        st_then = dexp_tinfer01(de0.arg2, ctx)
        st_else = dexp_tinfer01(de0.arg3, ctx)
        styp_unify(st_then, st_else)
        return st_then
    if de0.ctag == "DEfix":
        # Untyped fix: DEfix(f, x, body)
        f00 = de0.arg1
        x01 = de0.arg2
        st_arg = styp_new_xyz()
        st_res = styp_new_xyz()
        st_fun = styp_fun(st_arg, st_res)
        ctx1 = tctx_cons(f00, st_fun, ctx)
        ctx1 = tctx_cons(x01, st_arg, ctx1)
        st_body = dexp_tinfer01(de0.arg3, ctx1)
        styp_unify(st_res, st_body)
        return st_fun
    if de0.ctag == "DEfix1":
        # Typed fix: DEfix1(f, x, arg_type, body, res_type)
        f00 = de0.arg1
        x01 = de0.arg2
        st_arg = de0.arg3
        st_res = de0.arg5
        st_fun = styp_fun(st_arg, st_res)
        ctx1 = tctx_cons(f00, st_fun, ctx)
        ctx1 = tctx_cons(x01, st_arg, ctx1)
        st_body = dexp_tinfer01(de0.arg4, ctx1)
        styp_unify(st_res, st_body)
        return st_fun
    if de0.ctag == "DElet":
        x01 = de0.arg1
        st_def = dexp_tinfer01(de0.arg2, ctx)
        ctx1 = tctx_cons(x01, st_def, ctx)
        return dexp_tinfer01(de0.arg3, ctx1)
    if de0.ctag == "DElist_nil":
        alpha = styp_new_xyz()
        return styp_list(alpha)
    if de0.ctag == "DElist_cons":
        st_hd = dexp_tinfer01(de0.arg1, ctx)
        st_tl = dexp_tinfer01(de0.arg2, ctx)
        styp_unify(st_tl, styp_list(st_hd))
        return st_tl
    if de0.ctag == "DElazy":
        st0 = dexp_tinfer01(de0.arg1, ctx)
        return styp_lazy(st0)
    if de0.ctag == "DEstcn_nil":
        alpha = styp_new_xyz()
        return styp_stcn(alpha)
    if de0.ctag == "DEstcn_cons":
        st_hd = dexp_tinfer01(de0.arg1, ctx)
        st_tl = dexp_tinfer01(de0.arg2, ctx)
        # tail should be lazy(stcn(alpha))
        styp_unify(st_tl, styp_lazy(styp_stcn(st_hd)))
        return styp_stcn(st_hd)
    if de0.ctag == "DEarry_size_val":
        st_sz = dexp_tinfer01(de0.arg1, ctx)
        styp_unify(st_sz, styp_int)
        st_val = dexp_tinfer01(de0.arg2, ctx)
        return styp_arry(st_val)
    if de0.ctag == "DEarry_size_fun":
        st_sz = dexp_tinfer01(de0.arg1, ctx)
        styp_unify(st_sz, styp_int)
        st_fun = dexp_tinfer01(de0.arg2, ctx)
        alpha = styp_new_xyz()
        styp_unify(st_fun, styp_fun(styp_int, alpha))
        return styp_arry(alpha)
    if de0.ctag == "DEanno":
        st0 = dexp_tinfer01(de0.arg1, ctx)
        styp_unify(st0, de0.arg2)
        return de0.arg2
    raise TypeError("dexp_tinfer01: unhandled: " + de0.ctag)

############################################################
# JS Transpiler: dexp_trx2js
############################################################

class JSEmitter:
    def __init__(self):
        self.output = []
        self.indent = 0

    def emit(self, s):
        self.output.append(s)

    def emit_indent(self):
        self.emit("  " * self.indent)

    def emit_line(self, s):
        self.emit_indent()
        self.emit(s)
        self.emit("\n")

    def get_output(self):
        return "".join(self.output)

def _js_escape_str(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

def _js_opr_name(pnm):
    """Map operator name to JS expression, or None if inline."""
    return None  # We handle inline

def dexp_trx2js(de0):
    """Transpile dexp to JS code string."""
    em = JSEmitter()
    _emit_dexp(de0, em)
    return em.get_output()

def dexp_trx2js_print(de0):
    """Transpile and print JS code."""
    print(dexp_trx2js(de0))

def _emit_dexp(de0, em):
    """Emit JS expression for de0."""
    if de0.ctag == "DEint":
        em.emit(str(de0.arg1))
        return
    if de0.ctag == "DEbtf":
        em.emit("true" if de0.arg1 else "false")
        return
    if de0.ctag == "DEstr":
        em.emit('"' + _js_escape_str(de0.arg1) + '"')
        return
    if de0.ctag == "DEvar":
        em.emit(de0.arg1)
        return
    if de0.ctag == "DElam" or de0.ctag == "DElam1":
        x01 = de0.arg1
        body = de0.arg2 if de0.ctag == "DElam" else de0.arg3
        em.emit("(function(" + x01 + ") { return ")
        _emit_dexp(body, em)
        em.emit("; })")
        return
    if de0.ctag == "DEapp":
        _emit_dexp(de0.arg1, em)
        em.emit("(")
        _emit_dexp(de0.arg2, em)
        em.emit(")")
        return
    if de0.ctag == "DEopr":
        pnm = de0.arg1
        ags = de0.arg2
        # Binary infix operators
        if pnm in {"+", "-", "*", "/", "%"} and len(ags) == 2:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit(" " + pnm + " ")
            _emit_dexp(ags[1], em)
            em.emit(")")
            return
        if pnm in {"<", ">", "<=", ">="} and len(ags) == 2:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit(" " + pnm + " ")
            _emit_dexp(ags[1], em)
            em.emit(")")
            return
        if pnm == "=" and len(ags) == 2:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit(" === ")
            _emit_dexp(ags[1], em)
            em.emit(")")
            return
        if pnm == "!=" and len(ags) == 2:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit(" !== ")
            _emit_dexp(ags[1], em)
            em.emit(")")
            return
        if pnm == "&&" and len(ags) == 2:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit(" && ")
            _emit_dexp(ags[1], em)
            em.emit(")")
            return
        if pnm == "||" and len(ags) == 2:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit(" || ")
            _emit_dexp(ags[1], em)
            em.emit(")")
            return
        if pnm == "not" and len(ags) == 1:
            em.emit("(!")
            _emit_dexp(ags[0], em)
            em.emit(")")
            return
        if pnm == "neg" and len(ags) == 1:
            em.emit("(-")
            _emit_dexp(ags[0], em)
            em.emit(")")
            return
        if pnm == "cmp" and len(ags) == 2:
            # cmp(a, b) -> (a < b ? -1 : (a > b ? 1 : 0))
            em.emit("((")
            _emit_dexp(ags[0], em)
            em.emit(" < ")
            _emit_dexp(ags[1], em)
            em.emit(") ? -1 : ((")
            _emit_dexp(ags[0], em)
            em.emit(" > ")
            _emit_dexp(ags[1], em)
            em.emit(") ? 1 : 0))")
            return
        if pnm == "print":
            em.emit("console.log(")
            for i, a in enumerate(ags):
                if i > 0:
                    em.emit(", ")
                _emit_dexp(a, em)
            em.emit(")")
            return
        if pnm == "string_length" and len(ags) == 1:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit(".length)")
            return
        if pnm == "string_append" and len(ags) == 2:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit(" + ")
            _emit_dexp(ags[1], em)
            em.emit(")")
            return
        if pnm == "tostr" and len(ags) == 1:
            em.emit("String(")
            _emit_dexp(ags[0], em)
            em.emit(")")
            return
        # List operations
        if pnm == "list_length" and len(ags) == 1:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit(".length)")
            return
        if pnm == "list_head" and len(ags) == 1:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit("[0])")
            return
        if pnm == "list_tail" and len(ags) == 1:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit(".slice(1))")
            return
        # Array operations
        if pnm == "arry_get" and len(ags) == 2:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit("[")
            _emit_dexp(ags[1], em)
            em.emit("])")
            return
        if pnm == "arry_set" and len(ags) == 3:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit("[")
            _emit_dexp(ags[1], em)
            em.emit("] = ")
            _emit_dexp(ags[2], em)
            em.emit(")")
            return
        if pnm == "arry_length" and len(ags) == 1:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit(".length)")
            return
        # Lazy/stream
        if pnm == "lazy_force" and len(ags) == 1:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit("())")
            return
        if pnm == "stcn_head" and len(ags) == 1:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit("[0])")
            return
        if pnm == "stcn_tail" and len(ags) == 1:
            em.emit("(")
            _emit_dexp(ags[0], em)
            em.emit("[1])")
            return
        assert False, "Unknown operator for JS emit: " + pnm
    if de0.ctag == "DEfst":
        em.emit("(")
        _emit_dexp(de0.arg1, em)
        em.emit("[0])")
        return
    if de0.ctag == "DEsnd":
        em.emit("(")
        _emit_dexp(de0.arg1, em)
        em.emit("[1])")
        return
    if de0.ctag == "DEtup":
        em.emit("[")
        _emit_dexp(de0.arg1, em)
        em.emit(", ")
        _emit_dexp(de0.arg2, em)
        em.emit("]")
        return
    if de0.ctag == "DEif0":
        em.emit("(")
        _emit_dexp(de0.arg1, em)
        em.emit(" ? ")
        _emit_dexp(de0.arg2, em)
        em.emit(" : ")
        _emit_dexp(de0.arg3, em)
        em.emit(")")
        return
    if de0.ctag == "DEfix":
        # DEfix(f, x, body) -> named function expression
        f00 = de0.arg1
        x01 = de0.arg2
        body = de0.arg3
        em.emit("(function " + f00 + "(" + x01 + ") { return ")
        _emit_dexp(body, em)
        em.emit("; })")
        return
    if de0.ctag == "DEfix1":
        f00 = de0.arg1
        x01 = de0.arg2
        body = de0.arg4
        em.emit("(function " + f00 + "(" + x01 + ") { return ")
        _emit_dexp(body, em)
        em.emit("; })")
        return
    if de0.ctag == "DElet":
        x01 = de0.arg1
        em.emit("(function() { var " + x01 + " = ")
        _emit_dexp(de0.arg2, em)
        em.emit("; return ")
        _emit_dexp(de0.arg3, em)
        em.emit("; })()")
        return
    if de0.ctag == "DElist_nil":
        em.emit("[]")
        return
    if de0.ctag == "DElist_cons":
        em.emit("[")
        _emit_dexp(de0.arg1, em)
        em.emit("].concat(")
        _emit_dexp(de0.arg2, em)
        em.emit(")")
        return
    if de0.ctag == "DElazy":
        em.emit("(function() { return ")
        _emit_dexp(de0.arg1, em)
        em.emit("; })")
        return
    if de0.ctag == "DEstcn_nil":
        em.emit("null")
        return
    if de0.ctag == "DEstcn_cons":
        em.emit("[")
        _emit_dexp(de0.arg1, em)
        em.emit(", ")
        _emit_dexp(de0.arg2, em)
        em.emit("]")
        return
    if de0.ctag == "DEarry_size_val":
        em.emit("Array(")
        _emit_dexp(de0.arg1, em)
        em.emit(").fill(")
        _emit_dexp(de0.arg2, em)
        em.emit(")")
        return
    if de0.ctag == "DEarry_size_fun":
        em.emit("Array.from({length: ")
        _emit_dexp(de0.arg1, em)
        em.emit("}, function(_, i) { return (")
        _emit_dexp(de0.arg2, em)
        em.emit(")(i); })")
        return
    if de0.ctag == "DEanno":
        _emit_dexp(de0.arg1, em)
        return
    raise TypeError("dexp_trx2js: unhandled: " + de0.ctag)

############################################################
# Convenience constructors
############################################################

def DE_add(a, b): return dexp_opr("+", [a, b])
def DE_sub(a, b): return dexp_opr("-", [a, b])
def DE_mul(a, b): return dexp_opr("*", [a, b])
def DE_lt(a, b):  return dexp_opr("<", [a, b])
def DE_lte(a, b): return dexp_opr("<=", [a, b])
def DE_gt(a, b):  return dexp_opr(">", [a, b])
def DE_gte(a, b): return dexp_opr(">=", [a, b])
def DE_eq(a, b):  return dexp_opr("=", [a, b])

############################################################
# Tests
############################################################

def run_tests():
    print("=" * 60)
    print("TESTING TYPE INFERENCE")
    print("=" * 60)

    # Basic literals
    print("tinfer(DEint(1)) = " + str(dexp_tinfer(dexp_int(1))))
    print("tinfer(DEbtf(True)) = " + str(dexp_tinfer(dexp_btf(True))))
    print("tinfer(DEstr(\"hi\")) = " + str(dexp_tinfer(dexp_str("hi"))))

    # Arithmetic
    e_add = DE_add(dexp_int(1), dexp_int(2))
    print("tinfer(1+2) = " + str(dexp_tinfer(e_add)))

    # Comparison
    e_lte = DE_lte(dexp_int(1), dexp_int(2))
    print("tinfer(1<=2) = " + str(dexp_tinfer(e_lte)))

    # Typed lambda: lam(x:int). x+x
    var_x = dexp_var("x")
    e_dbl = dexp_lam1("x", styp_int, DE_add(var_x, var_x))
    print("tinfer(dbl) = " + str(dexp_tinfer(e_dbl)))

    # Untyped lambda: lam(x). x+x  (should infer int->int)
    e_dbl2 = dexp_lam("x", DE_add(var_x, var_x))
    print("tinfer(dbl_untyped) = " + str(dexp_tinfer(e_dbl2)))

    # Application
    e_app = dexp_app(e_dbl2, dexp_int(5))
    print("tinfer(dbl(5)) = " + str(dexp_tinfer(e_app)))

    # Tuple
    e_tup = dexp_tup(dexp_int(1), dexp_btf(True))
    print("tinfer((1, true)) = " + str(dexp_tinfer(e_tup)))

    # Fst/Snd
    e_fst = dexp_fst(e_tup)
    print("tinfer(fst(1, true)) = " + str(dexp_tinfer(e_fst)))
    e_snd = dexp_snd(e_tup)
    print("tinfer(snd(1, true)) = " + str(dexp_tinfer(e_snd)))

    # If0
    e_if = dexp_if0(dexp_btf(True), dexp_int(1), dexp_int(2))
    print("tinfer(if true then 1 else 2) = " + str(dexp_tinfer(e_if)))

    # Let
    e_let = dexp_let("x", dexp_int(42), DE_add(dexp_var("x"), dexp_int(1)))
    print("tinfer(let x=42 in x+1) = " + str(dexp_tinfer(e_let)))

    var_f = dexp_var("f")
    var_n = dexp_var("n")
    e_fact1 = dexp_fix1("f", "n", styp_int,
        dexp_if0(DE_lte(var_n, dexp_int(0)),
            dexp_int(1),
            DE_mul(var_n, dexp_app(var_f, DE_sub(var_n, dexp_int(1))))),
        styp_int)
    print("tinfer(fact1) = " + str(dexp_tinfer(e_fact1)))

    e_fact = dexp_fix("f", "n",
        dexp_if0(DE_lte(var_n, dexp_int(0)),
            dexp_int(1),
            DE_mul(var_n, dexp_app(var_f, DE_sub(var_n, dexp_int(1))))))
    print("tinfer(fact_untyped) = " + str(dexp_tinfer(e_fact)))

    e_id = dexp_lam("x", dexp_var("x"))
    print("tinfer(id) = " + str(dexp_tinfer(e_id)))

    # List
    e_nil = dexp_list_nil()
    print("tinfer(nil) = " + str(dexp_tinfer(e_nil)))
    e_cons = dexp_list_cons(dexp_int(1), dexp_list_nil())
    print("tinfer(cons(1, nil)) = " + str(dexp_tinfer(e_cons)))

    # Anno
    e_anno = dexp_anno(dexp_int(42), styp_int)
    print("tinfer(anno(42, int)) = " + str(dexp_tinfer(e_anno)))

    # Lazy
    e_lazy = dexp_lazy(dexp_int(42))
    print("tinfer(lazy(42)) = " + str(dexp_tinfer(e_lazy)))

    # tail-recursive fact2 (from reference)
    var_i = dexp_var("i")
    var_r = dexp_var("r")
    styp_fun_int_int = styp_fun(styp_int, styp_int)
    e_fact2 = \
        dexp_lam1("n", styp_int,
            dexp_app(
                dexp_app(
                    dexp_fix1("f", "i", styp_int,
                        dexp_lam1("r", styp_int,
                            dexp_if0(DE_gte(var_i, var_n),
                                var_r,
                                dexp_app(
                                    dexp_app(var_f, DE_add(var_i, dexp_int(1))),
                                    DE_mul(DE_add(var_i, dexp_int(1)), var_r)))),
                        styp_fun_int_int),
                    dexp_int(1)),
                dexp_int(1)))
    print("tinfer(fact2) = " + str(dexp_tinfer(e_fact2)))

    # Church numeral 3
    e_ch3 = dexp_lam1("f", styp_fun_int_int,
        dexp_lam1("x", styp_int,
            dexp_app(var_f,
                dexp_app(var_f,
                    dexp_app(var_f, dexp_var("x"))))))
    print("tinfer(CHNUM3) = " + str(dexp_tinfer(e_ch3)))

    print()
    print("=" * 60)
    print("TESTING JS TRANSPILATION")
    print("=" * 60)

    # Basic
    print("--- int literal ---")
    print(dexp_trx2js(dexp_int(42)))

    print("--- bool literal ---")
    print(dexp_trx2js(dexp_btf(True)))

    print("--- string literal ---")
    print(dexp_trx2js(dexp_str("hello")))

    print("--- add ---")
    print(dexp_trx2js(DE_add(dexp_int(1), dexp_int(2))))

    print("--- lam (typed) ---")
    print(dexp_trx2js(e_dbl))

    print("--- lam (untyped) ---")
    print(dexp_trx2js(e_dbl2))

    print("--- app ---")
    print(dexp_trx2js(e_app))

    print("--- tuple ---")
    print(dexp_trx2js(e_tup))

    print("--- fst ---")
    print(dexp_trx2js(e_fst))

    print("--- if ---")
    print(dexp_trx2js(e_if))

    print("--- let ---")
    print(dexp_trx2js(e_let))

    print("--- fact (typed fix) ---")
    js_fact1 = dexp_trx2js(e_fact1)
    print(js_fact1)

    print("--- fact (untyped fix) ---")
    js_fact = dexp_trx2js(e_fact)
    print(js_fact)

    print("--- fact2 (tail-recursive) ---")
    js_fact2 = dexp_trx2js(e_fact2)
    print(js_fact2)

    print("--- list ---")
    e_list = dexp_list_cons(dexp_int(1), dexp_list_cons(dexp_int(2), dexp_list_nil()))
    print(dexp_trx2js(e_list))

    print("--- lazy ---")
    print(dexp_trx2js(e_lazy))

    print("--- stream cons ---")
    e_stcn = dexp_stcn_cons(dexp_int(1), dexp_lazy(dexp_stcn_nil()))
    print(dexp_trx2js(e_stcn))

    print("--- array_size_val ---")
    print(dexp_trx2js(dexp_arry_size_val(dexp_int(10), dexp_int(0))))

    print("--- array_size_fun ---")
    e_af = dexp_arry_size_fun(dexp_int(10), dexp_lam("i", dexp_var("i")))
    print(dexp_trx2js(e_af))

    # Generate runnable JS for fact
    print()
    print("=" * 60)
    print("RUNNABLE JS EXAMPLES")
    print("=" * 60)

    print("// fact(10):")
    print("console.log((" + js_fact + ")(10));")
    print()
    print("// fact2(10):")
    print("console.log((" + js_fact2 + ")(10));")

if __name__ == "__main__":
    run_tests()

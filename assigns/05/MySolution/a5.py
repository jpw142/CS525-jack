############################################################
############################################################
#
# Assign05 for CS525, Spring, 2026
# It is due Tuesday, the 14th of March, 2026
# Midterm-1 Project:
# Compile extended lambda-calculus to pure lambda-calculus
#
############################################################
############################################################

import sys
sys.setrecursionlimit(200000)

############################################################
# Term definitions (same as assign04)
############################################################

class term:
    ctag = ""

class term_var(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMvar"
    def __str__(self):
        return f"TMvar({self.arg1})"

class term_lam(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMlam"
    def __str__(self):
        return f"TMlam({self.arg1}, {self.arg2})"

class term_app(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMapp"
    def __str__(self):
        return f"TMapp({self.arg1}, {self.arg2})"

class term_int(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMint"
    def __str__(self):
        return f"TMint({self.arg1})"

class term_btf(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMbtf"
    def __str__(self):
        return f"TMbtf({self.arg1})"

class term_opr(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMopr"
    def __str__(self):
        args = ", ".join(str(a) for a in self.arg2)
        return f"TMopr({self.arg1}, [{args}])"

class term_tup(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMtup"
    def __str__(self):
        return f"TMtup({self.arg1}, {self.arg2})"

class term_fst(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMfst"
    def __str__(self):
        return f"TMfst({self.arg1})"

class term_snd(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMsnd"
    def __str__(self):
        return f"TMsnd({self.arg1})"

class term_if0(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TMif0"
    def __str__(self):
        return f"TMif0({self.arg1}, {self.arg2}, {self.arg3})"

class term_fix(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TMfix"
    def __str__(self):
        return f"TMfix({self.arg1}, {self.arg2}, {self.arg3})"

class term_let(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TMlet"
    def __str__(self):
        return f"TMlet({self.arg1}, {self.arg2}, {self.arg3})"

############################################################
# Constructors
############################################################

def TMvar(x): return term_var(x)
def TMlam(x, body): return term_lam(x, body)
def TMapp(t1, t2): return term_app(t1, t2)
def TMint(n): return term_int(n)
def TMbtf(b): return term_btf(b)
def TMopr(name, args): return term_opr(name, args)
def TMtup(t1, t2): return term_tup(t1, t2)
def TMfst(t): return term_fst(t)
def TMsnd(t): return term_snd(t)
def TMif0(t1, t2, t3): return term_if0(t1, t2, t3)
def TMfix(f, x, body): return term_fix(f, x, body)
def TMlet(x, t1, t2): return term_let(x, t1, t2)

############################################################
# Check if a term is pure (only TMvar, TMlam, TMapp)
############################################################

def is_pure(tm):
    if tm.ctag == "TMvar":
        return True
    if tm.ctag == "TMlam":
        return is_pure(tm.arg2)
    if tm.ctag == "TMapp":
        return is_pure(tm.arg1) and is_pure(tm.arg2)
    return False

############################################################
############################################################
#
# Church Encodings
#
############################################################
############################################################

# ---- Church numerals ----
# n = lam f. lam x. f(f(...(f x)...))

def church_numeral(n):
    body = TMvar("x")
    for _ in range(n):
        body = TMapp(TMvar("f"), body)
    return TMlam("f", TMlam("x", body))

# ---- Church booleans ----
# true  = lam t. lam f. t
# false = lam t. lam f. f

def church_true():
    return TMlam("ct", TMlam("cf", TMvar("ct")))

def church_false():
    return TMlam("ct", TMlam("cf", TMvar("cf")))

# ---- Church pairs ----
# pair = lam a. lam b. lam s. s a b
# fst  = lam p. p (lam a. lam b. a)
# snd  = lam p. p (lam a. lam b. b)

def church_pair():
    return TMlam("pa", TMlam("pb", TMlam("ps",
        TMapp(TMapp(TMvar("ps"), TMvar("pa")), TMvar("pb"))
    )))

def church_fst():
    return TMlam("pp", TMapp(TMvar("pp"),
        TMlam("pa", TMlam("pb", TMvar("pa")))
    ))

def church_snd():
    return TMlam("pp", TMapp(TMvar("pp"),
        TMlam("pa", TMlam("pb", TMvar("pb")))
    ))

# ---- Successor ----
# succ = lam n. lam f. lam x. f (n f x)

def church_succ():
    return TMlam("sn", TMlam("sf", TMlam("sx",
        TMapp(TMvar("sf"),
              TMapp(TMapp(TMvar("sn"), TMvar("sf")), TMvar("sx")))
    )))

# ---- Addition ----
# add = lam m. lam n. lam f. lam x. m f (n f x)

def church_add():
    return TMlam("am", TMlam("an", TMlam("af", TMlam("ax",
        TMapp(TMapp(TMvar("am"), TMvar("af")),
              TMapp(TMapp(TMvar("an"), TMvar("af")), TMvar("ax")))
    ))))

# ---- Multiplication ----
# mul = lam m. lam n. lam f. m (n f)

def church_mul():
    return TMlam("mm", TMlam("mn", TMlam("mf",
        TMapp(TMvar("mm"), TMapp(TMvar("mn"), TMvar("mf")))
    )))

# ---- Predecessor (pair technique) ----
# pred = lam n. fst (n step init)
#   step = lam p. pair (snd p) (succ (snd p))
#   init = pair 0 0

def church_pred():
    snd_p = TMapp(church_snd(), TMvar("pp"))
    step = TMlam("pp",
        TMapp(TMapp(church_pair(), snd_p),
              TMapp(church_succ(), snd_p))
    )
    init = TMapp(TMapp(church_pair(), church_numeral(0)), church_numeral(0))
    return TMlam("pn",
        TMapp(church_fst(),
              TMapp(TMapp(TMvar("pn"), step), init))
    )

# ---- Subtraction ----
# sub = lam m. lam n. n pred m

def church_sub():
    return TMlam("sm", TMlam("sn",
        TMapp(TMapp(TMvar("sn"), church_pred()), TMvar("sm"))
    ))

# ---- IsZero ----
# iszero = lam n. n (lam x. false) true

def church_iszero():
    return TMlam("zn",
        TMapp(TMapp(TMvar("zn"),
                    TMlam("zx", church_false())),
              church_true())
    )

# ---- Comparisons ----

# leq(m,n) = iszero(sub(m,n))
def church_leq():
    return TMlam("lm", TMlam("ln",
        TMapp(church_iszero(),
              TMapp(TMapp(church_sub(), TMvar("lm")), TMvar("ln")))
    ))

# and = lam a. lam b. a b false
def church_and():
    return TMlam("aa", TMlam("ab",
        TMapp(TMapp(TMvar("aa"), TMvar("ab")), church_false())
    ))

# not = lam a. a false true
def church_not():
    return TMlam("na",
        TMapp(TMapp(TMvar("na"), church_false()), church_true())
    )

# eq(m,n) = and (leq m n) (leq n m)
def church_eq():
    return TMlam("em", TMlam("en",
        TMapp(TMapp(church_and(),
                    TMapp(TMapp(church_leq(), TMvar("em")), TMvar("en"))),
              TMapp(TMapp(church_leq(), TMvar("en")), TMvar("em")))
    ))

# lt(m,n) = not(leq(n,m))
def church_lt():
    return TMlam("lm", TMlam("ln",
        TMapp(church_not(),
              TMapp(TMapp(church_leq(), TMvar("ln")), TMvar("lm")))
    ))

# gt(m,n) = not(leq(m,n))
def church_gt():
    return TMlam("gm", TMlam("gn",
        TMapp(church_not(),
              TMapp(TMapp(church_leq(), TMvar("gm")), TMvar("gn")))
    ))

# geq(m,n) = leq(n,m)
def church_geq():
    return TMlam("gm", TMlam("gn",
        TMapp(TMapp(church_leq(), TMvar("gn")), TMvar("gm"))
    ))

# neq(m,n) = not(eq(m,n))
def church_neq():
    return TMlam("nm", TMlam("nn",
        TMapp(church_not(),
              TMapp(TMapp(church_eq(), TMvar("nm")), TMvar("nn")))
    ))

# ---- Z combinator (call-by-value Y combinator) ----
# Z = lam f. (lam x. f (lam v. x x v)) (lam x. f (lam v. x x v))

def z_combinator():
    inner = TMlam("zx",
        TMapp(TMvar("zf"),
              TMlam("zv", TMapp(TMapp(TMvar("zx"), TMvar("zx")), TMvar("zv"))))
    )
    return TMlam("zf", TMapp(inner, inner))

# ---- Division (recursive via Z) ----
# div(m, n) = if leq(n,m) then 1 + div(m-n, n) else 0

def church_div():
    I = TMlam("di", TMvar("di"))
    m = TMvar("dm")
    n = TMvar("dn")
    div_f = TMvar("df")
    cond = TMapp(TMapp(church_leq(), n), m)
    then_br = TMlam("d1",
        TMapp(church_succ(),
              TMapp(TMapp(div_f, TMapp(TMapp(church_sub(), m), n)), n)))
    else_br = TMlam("d2", church_numeral(0))
    body = TMapp(TMapp(TMapp(cond, then_br), else_br), I)
    return TMapp(z_combinator(), TMlam("df", TMlam("dm", TMlam("dn", body))))

# ---- Modulo (recursive via Z) ----
# mod(m, n) = if leq(n,m) then mod(m-n, n) else m

def church_mod():
    I = TMlam("mi", TMvar("mi"))
    m = TMvar("rm")
    n = TMvar("rn")
    mod_f = TMvar("rf")
    cond = TMapp(TMapp(church_leq(), n), m)
    then_br = TMlam("r1",
        TMapp(TMapp(mod_f, TMapp(TMapp(church_sub(), m), n)), n))
    else_br = TMlam("r2", m)
    body = TMapp(TMapp(TMapp(cond, then_br), else_br), I)
    return TMapp(z_combinator(), TMlam("rf", TMlam("rm", TMlam("rn", body))))


############################################################
############################################################
#
# THE COMPILER
#
############################################################
############################################################

def assign05_compile(source):
    """
    Compile an extended lambda-calculus term into a
    pure lambda-calculus term (only TMvar, TMlam, TMapp).
    """
    return compile(source)

def compile(tm):
    tag = tm.ctag

    # pure terms: just recurse into subterms
    if tag == "TMvar":
        return tm
    if tag == "TMlam":
        return TMlam(tm.arg1, compile(tm.arg2))
    if tag == "TMapp":
        return TMapp(compile(tm.arg1), compile(tm.arg2))

    # integers -> Church numerals
    if tag == "TMint":
        return church_numeral(tm.arg1)

    # booleans -> Church booleans
    if tag == "TMbtf":
        if tm.arg1:
            return church_true()
        else:
            return church_false()

    # tuples -> Church pairs
    if tag == "TMtup":
        a = compile(tm.arg1)
        b = compile(tm.arg2)
        return TMapp(TMapp(church_pair(), a), b)
    if tag == "TMfst":
        return TMapp(church_fst(), compile(tm.arg1))
    if tag == "TMsnd":
        return TMapp(church_snd(), compile(tm.arg1))

    # let x = e1 in e2  =>  (lam x. [[e2]]) [[e1]]
    if tag == "TMlet":
        x = tm.arg1
        e1 = compile(tm.arg2)
        e2 = compile(tm.arg3)
        return TMapp(TMlam(x, e2), e1)

    # if-then-else with thunks for call-by-value
    # [[cond]] (lam _. [[then]]) (lam _. [[else]]) (lam x. x)
    if tag == "TMif0":
        c = compile(tm.arg1)
        t = compile(tm.arg2)
        e = compile(tm.arg3)
        thunk_t = TMlam("_t", t)
        thunk_e = TMlam("_e", e)
        I = TMlam("_i", TMvar("_i"))
        return TMapp(TMapp(TMapp(c, thunk_t), thunk_e), I)

    # TMfix(f, x, body) => Z (lam f. lam x. [[body]])
    if tag == "TMfix":
        f = tm.arg1
        x = tm.arg2
        body = compile(tm.arg3)
        return TMapp(z_combinator(), TMlam(f, TMlam(x, body)))

    # arithmetic and comparisons
    if tag == "TMopr":
        op = tm.arg1
        args = [compile(a) for a in tm.arg2]
        if op == "+":
            return TMapp(TMapp(church_add(), args[0]), args[1])
        if op == "-":
            return TMapp(TMapp(church_sub(), args[0]), args[1])
        if op == "*":
            return TMapp(TMapp(church_mul(), args[0]), args[1])
        if op == "/":
            return TMapp(TMapp(church_div(), args[0]), args[1])
        if op == "%":
            return TMapp(TMapp(church_mod(), args[0]), args[1])
        if op == "=":
            return TMapp(TMapp(church_eq(), args[0]), args[1])
        if op == "!=":
            return TMapp(TMapp(church_neq(), args[0]), args[1])
        if op == "<":
            return TMapp(TMapp(church_lt(), args[0]), args[1])
        if op == ">":
            return TMapp(TMapp(church_gt(), args[0]), args[1])
        if op == "<=":
            return TMapp(TMapp(church_leq(), args[0]), args[1])
        if op == ">=":
            return TMapp(TMapp(church_geq(), args[0]), args[1])
        raise ValueError(f"Unknown operator: {op}")

    raise TypeError(f"Unknown term: {tag}")


############################################################
############################################################
#
# CBV evaluator for testing compiled (pure) terms
#
############################################################
############################################################

class Closure:
    def __init__(self, var, body, env):
        self.var = var
        self.body = body
        self.env = env

class PyVal:
    """Wrapper so we can inject Python values into the LC evaluator."""
    def __init__(self, v):
        self.v = v

def cbv_eval(tm, env, fuel):
    """Call-by-value evaluator for pure lambda terms."""
    fuel[0] -= 1 # prevent infinite recrsuion
    if fuel[0] <= 0:
        raise RuntimeError("out of fuel")
    if tm.ctag == "TMvar":
        return env[tm.arg1]
    if tm.ctag == "TMlam":
        return Closure(tm.arg1, tm.arg2, dict(env))
    if tm.ctag == "TMapp":
        fn = cbv_eval(tm.arg1, env, fuel)
        arg = cbv_eval(tm.arg2, env, fuel)
        if isinstance(fn, Closure):
            new_env = dict(fn.env)
            new_env[fn.var] = arg
            return cbv_eval(fn.body, new_env, fuel)
        if isinstance(fn, PyVal) and callable(fn.v):
            if isinstance(arg, PyVal):
                return PyVal(fn.v(arg.v))
            return PyVal(fn.v(arg))
        raise ValueError(f"cannot apply {type(fn)}")
    raise TypeError(f"unknown: {tm.ctag}")

def eval_to_int(compiled, fuel_amt=500000):
    """
    Church numeral n applied to (+1) and 0 gives n.
    """
    fuel = [fuel_amt]
    val = cbv_eval(compiled, {}, fuel)
    if not isinstance(val, Closure):
        return None
    # apply to successor
    env1 = dict(val.env)
    env1[val.var] = PyVal(lambda n: n + 1)
    val2 = cbv_eval(val.body, env1, fuel)
    if not isinstance(val2, Closure):
        return None
    # apply to zero
    env2 = dict(val2.env)
    env2[val2.var] = PyVal(0)
    result = cbv_eval(val2.body, env2, fuel)
    if isinstance(result, PyVal) and isinstance(result.v, int):
        return result.v
    return None

def eval_to_bool(compiled, fuel_amt=500000):
    """
    Church true applied to True, False gives True. Etc.
    """
    fuel = [fuel_amt]
    val = cbv_eval(compiled, {}, fuel)
    if not isinstance(val, Closure):
        return None
    env1 = dict(val.env)
    env1[val.var] = PyVal(True)
    val2 = cbv_eval(val.body, env1, fuel)
    if not isinstance(val2, Closure):
        return None
    env2 = dict(val2.env)
    env2[val2.var] = PyVal(False)
    result = cbv_eval(val2.body, env2, fuel)
    if isinstance(result, PyVal):
        return result.v
    return None


############################################################
# Test helper
############################################################

def test(label, source, expected, fuel=500000):
    compiled = assign05_compile(source)
    assert is_pure(compiled), f"{label}: not pure!"
    try:
        if isinstance(expected, bool):
            result = eval_to_bool(compiled, fuel)
        else:
            result = eval_to_int(compiled, fuel)
        if result == expected:
            print(f"  {label}: OK ({result})")
        else:
            print(f"  {label}: FAIL (expected {expected}, got {result})")
    except RuntimeError:
        print(f"  {label}: TIMEOUT")
    except Exception as e:
        print(f"  {label}: ERROR ({e})")


############################################################
# Tests
############################################################

def test_basics():
    print("=== Basic Tests ===")
    test("int(0)", TMint(0), 0)
    test("int(3)", TMint(3), 3)
    test("int(5)", TMint(5), 5)
    test("true", TMbtf(True), True)
    test("false", TMbtf(False), False)
    test("2+3", TMopr("+", [TMint(2), TMint(3)]), 5)
    test("5-2", TMopr("-", [TMint(5), TMint(2)]), 3)
    test("3*4", TMopr("*", [TMint(3), TMint(4)]), 12)
    test("10/3", TMopr("/", [TMint(10), TMint(3)]), 3)
    test("7%3", TMopr("%", [TMint(7), TMint(3)]), 1)
    test("3=3", TMopr("=", [TMint(3), TMint(3)]), True)
    test("3=4", TMopr("=", [TMint(3), TMint(4)]), False)
    test("3<4", TMopr("<", [TMint(3), TMint(4)]), True)
    test("3>2", TMopr(">", [TMint(3), TMint(2)]), True)
    test("fst(3,5)", TMfst(TMtup(TMint(3), TMint(5))), 3)
    test("snd(3,5)", TMsnd(TMtup(TMint(3), TMint(5))), 5)
    test("let x=3 in x+x",
         TMlet("x", TMint(3), TMopr("+", [TMvar("x"), TMvar("x")])), 6)
    test("if true then 1 else 2",
         TMif0(TMbtf(True), TMint(1), TMint(2)), 1)
    test("if false then 1 else 2",
         TMif0(TMbtf(False), TMint(1), TMint(2)), 2)
    test("if 3=3 then 10 else 20",
         TMif0(TMopr("=", [TMint(3), TMint(3)]), TMint(10), TMint(20)), 10)
    test("if 3=4 then 10 else 20",
         TMif0(TMopr("=", [TMint(3), TMint(4)]), TMint(10), TMint(20)), 20)
    print()

def test_factorial():
    print("=== Factorial ===")
    # fun fact(n) = if n = 0 then 1 else n * fact(n-1)
    factorial = TMfix("fact", "n",
        TMif0(
            TMopr("=", [TMvar("n"), TMint(0)]),
            TMint(1),
            TMopr("*", [
                TMvar("n"),
                TMapp(TMvar("fact"),
                      TMopr("-", [TMvar("n"), TMint(1)]))])))
    test("fact(0)", TMapp(factorial, TMint(0)), 1)
    test("fact(1)", TMapp(factorial, TMint(1)), 1)
    test("fact(2)", TMapp(factorial, TMint(2)), 2)
    test("fact(3)", TMapp(factorial, TMint(3)), 6)
    test("fact(4)", TMapp(factorial, TMint(4)), 24)
    test("fact(5)", TMapp(factorial, TMint(5)), 120)
    print()

def test_fibonacci():
    print("=== Fibonacci ===")
    # fun fib(n) = if n=0 then 0 else if n=1 then 1 else fib(n-1)+fib(n-2)
    fib = TMfix("fib", "n",
        TMif0(
            TMopr("=", [TMvar("n"), TMint(0)]),
            TMint(0),
            TMif0(
                TMopr("=", [TMvar("n"), TMint(1)]),
                TMint(1),
                TMopr("+", [
                    TMapp(TMvar("fib"),
                          TMopr("-", [TMvar("n"), TMint(1)])),
                    TMapp(TMvar("fib"),
                          TMopr("-", [TMvar("n"), TMint(2)]))]))))
    test("fib(0)", TMapp(fib, TMint(0)), 0)
    test("fib(1)", TMapp(fib, TMint(1)), 1)
    test("fib(2)", TMapp(fib, TMint(2)), 1)
    test("fib(3)", TMapp(fib, TMint(3)), 2)
    test("fib(4)", TMapp(fib, TMint(4)), 3)
    test("fib(5)", TMapp(fib, TMint(5)), 5)
    test("fib(6)", TMapp(fib, TMint(6)), 8)
    test("fib(7)", TMapp(fib, TMint(7)), 13)
    print()

def test_power():
    print("=== Power ===")
    # fun power(x, n) = if n > 0 then x * power(x, n-1) else 1
    # TMfix only takes one arg so we use a tuple
    power = TMfix("pow", "args",
        TMlet("x", TMfst(TMvar("args")),
        TMlet("n", TMsnd(TMvar("args")),
            TMif0(
                TMopr(">", [TMvar("n"), TMint(0)]),
                TMopr("*", [
                    TMvar("x"),
                    TMapp(TMvar("pow"),
                          TMtup(TMvar("x"),
                                TMopr("-", [TMvar("n"), TMint(1)])))]),
                TMint(1)))))
    def pw(x, n):
        return TMapp(power, TMtup(TMint(x), TMint(n)))
    test("power(2,0)", pw(2, 0), 1)
    test("power(2,1)", pw(2, 1), 2)
    test("power(2,2)", pw(2, 2), 4)
    test("power(2,3)", pw(2, 3), 8)
    test("power(3,2)", pw(3, 2), 9)
    test("power(3,3)", pw(3, 3), 27)
    test("power(2,10)", pw(2, 10), 1024)
    print()

def test_purity():
    print("=== Purity Check ===")
    terms = [
        TMint(5), TMbtf(True), TMopr("+", [TMint(2), TMint(3)]),
        TMtup(TMint(1), TMint(2)), TMfst(TMtup(TMint(1), TMint(2))),
        TMif0(TMbtf(True), TMint(1), TMint(2)),
        TMlet("x", TMint(3), TMvar("x")),
        TMfix("f", "x", TMvar("x")),
    ]
    ok = True
    for t in terms:
        c = assign05_compile(t)
        if not is_pure(c):
            print(f"  NOT PURE: {t}")
            ok = False
    if ok:
        print("  All compiled terms are pure. OK")
    print()


if __name__ == "__main__":
    test_purity()
    test_basics()
    test_factorial()
    test_fibonacci()
    test_power()
    print("Done.")

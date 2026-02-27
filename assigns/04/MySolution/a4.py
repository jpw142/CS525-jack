############################################################
############################################################
#
# Assign04 for CS525, Spring, 2026
# It is due the 26th of February, 2026
#
############################################################
############################################################

############################################################
# term datatype
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

class term_str(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMstr"
    def __str__(self):
        return f"TMstr({repr(self.arg1)})"

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

class term_let(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TMlet"
    def __str__(self):
        return f"TMlet({self.arg1}, {self.arg2}, {self.arg3})"

class term_fix(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TMfix"
    def __str__(self):
        return f"TMfix({self.arg1}, {self.arg2}, {self.arg3})"

############################################################

def TMvar(x): return term_var(x)
def TMlam(x, body): return term_lam(x, body)
def TMapp(t1, t2): return term_app(t1, t2)
def TMint(n): return term_int(n)
def TMbtf(b): return term_btf(b)
def TMstr(s): return term_str(s)
def TMopr(name, args): return term_opr(name, args)
def TMtup(t1, t2): return term_tup(t1, t2)
def TMfst(t): return term_fst(t)
def TMsnd(t): return term_snd(t)
def TMif0(t1, t2, t3): return term_if0(t1, t2, t3)
def TMlet(x, t1, t2): return term_let(x, t1, t2)
def TMfix(f, x, body): return term_fix(f, x, body)

############################################################
# value forms
############################################################

class VALint:
    def __init__(self, n): self.n = n
    def __str__(self): return f"VALint({self.n})"

class VALbtf:
    def __init__(self, b): self.b = b
    def __str__(self): return f"VALbtf({self.b})"

class VALstr:
    def __init__(self, s): self.s = s
    def __str__(self): return f"VALstr({repr(self.s)})"

class VALtup:
    def __init__(self, v1, v2): self.v1 = v1; self.v2 = v2
    def __str__(self): return f"VALtup({self.v1}, {self.v2})"

class VALlam:
    def __init__(self, x, body, env):
        self.x = x; self.body = body; self.env = env
    def __str__(self): return f"VALlam({self.x}, ...)"

class VALfix:
    def __init__(self, f, x, body, env):
        self.f = f; self.x = x; self.body = body; self.env = env
    def __str__(self): return f"VALfix({self.f}, {self.x}, ...)"

############################################################
# 4-1: call-by-value evaluator
############################################################

def lambda_eval(tm0, env=None):
    if env is None:
        env = {}
    stack = []
    cur_tm = tm0
    cur_env = env
    while True:
        result = _eval_step(cur_tm, cur_env, stack)
        if result[0] == "CONTINUE":
            cur_tm, cur_env = result[1], result[2]
        elif result[0] == "VALUE":
            val = result[1]
            while stack:
                cont = stack.pop()
                nxt = cont(val)
                if nxt[0] == "CONTINUE":
                    cur_tm, cur_env = nxt[1], nxt[2]
                    break
                val = nxt[1]
            else:
                return val

def _eval_step(tm0, env, stack):
    tag = tm0.ctag

    if tag == "TMvar":
        x = tm0.arg1
        if x in env:
            return ("VALUE", env[x])
        raise RuntimeError(f"Unbound variable: {x}")

    if tag == "TMlam":
        return ("VALUE", VALlam(tm0.arg1, tm0.arg2, env.copy()))

    if tag == "TMapp":
        t1, t2 = tm0.arg1, tm0.arg2
        cur_env = env
        # eval t1, then t2, then apply
        def app_cont1(fval, t2=t2, cur_env=cur_env):
            def app_cont2(aval, fval=fval):
                if isinstance(fval, VALlam):
                    new_env = fval.env.copy()
                    new_env[fval.x] = aval
                    return ("CONTINUE", fval.body, new_env)
                elif isinstance(fval, VALfix):
                    new_env = fval.env.copy()
                    new_env[fval.f] = fval  # bind f to itself
                    new_env[fval.x] = aval
                    return ("CONTINUE", fval.body, new_env)
                else:
                    raise RuntimeError(f"Application of non-function: {fval}")
            stack.append(app_cont2)
            return ("CONTINUE", t2, cur_env)
        stack.append(app_cont1)
        return ("CONTINUE", t1, env)

    if tag == "TMint":
        return ("VALUE", VALint(tm0.arg1))

    if tag == "TMbtf":
        return ("VALUE", VALbtf(tm0.arg1))

    if tag == "TMstr":
        return ("VALUE", VALstr(tm0.arg1))

    if tag == "TMopr":
        opr = tm0.arg1
        args = tm0.arg2
        if len(args) == 0:
            return ("VALUE", eval_opr(opr, []))
        vals = []
        def make_arg_cont(remaining_args, vals, opr, env):
            def cont(v):
                vals.append(v)
                if not remaining_args:
                    return ("VALUE", eval_opr(opr, vals))
                nxt_arg = remaining_args.pop(0)
                stack.append(make_arg_cont(remaining_args, vals, opr, env))
                return ("CONTINUE", nxt_arg, env)
            return cont
        remaining = list(args[1:])
        stack.append(make_arg_cont(remaining, vals, opr, env))
        return ("CONTINUE", args[0], env)

    if tag == "TMtup":
        t1, t2 = tm0.arg1, tm0.arg2
        cur_env = env
        def tup_cont1(v1, t2=t2, cur_env=cur_env):
            def tup_cont2(v2, v1=v1):
                return ("VALUE", VALtup(v1, v2))
            stack.append(tup_cont2)
            return ("CONTINUE", t2, cur_env)
        stack.append(tup_cont1)
        return ("CONTINUE", t1, env)

    if tag == "TMfst":
        def fst_cont(v):
            if isinstance(v, VALtup):
                return ("VALUE", v.v1)
            raise RuntimeError(f"fst of non-tuple: {v}")
        stack.append(fst_cont)
        return ("CONTINUE", tm0.arg1, env)

    if tag == "TMsnd":
        def snd_cont(v):
            if isinstance(v, VALtup):
                return ("VALUE", v.v2)
            raise RuntimeError(f"snd of non-tuple: {v}")
        stack.append(snd_cont)
        return ("CONTINUE", tm0.arg1, env)

    if tag == "TMif0":
        cond, then_br, else_br = tm0.arg1, tm0.arg2, tm0.arg3
        cur_env = env
        def if_cont(cv, then_br=then_br, else_br=else_br, cur_env=cur_env):
            if isinstance(cv, VALbtf):
                return ("CONTINUE", then_br if cv.b else else_br, cur_env)
            elif isinstance(cv, VALint):
                return ("CONTINUE", then_br if cv.n == 0 else else_br, cur_env)
            else:
                raise RuntimeError(f"if0 on non-bool/int: {cv}")
        stack.append(if_cont)
        return ("CONTINUE", cond, env)

    if tag == "TMlet":
        x, defn, body = tm0.arg1, tm0.arg2, tm0.arg3
        cur_env = env
        def let_cont(v, x=x, body=body, cur_env=cur_env):
            new_env = cur_env.copy()
            new_env[x] = v
            return ("CONTINUE", body, new_env)
        stack.append(let_cont)
        return ("CONTINUE", defn, env)

    if tag == "TMfix":
        return ("VALUE", VALfix(tm0.arg1, tm0.arg2, tm0.arg3, env.copy()))

    raise RuntimeError(f"Unknown term: {tag}")


def eval_opr(opr, vals):
    if opr == "+" and len(vals) == 2:
        return VALint(vals[0].n + vals[1].n)
    if opr == "-" and len(vals) == 2:
        return VALint(vals[0].n - vals[1].n)
    if opr == "*" and len(vals) == 2:
        return VALint(vals[0].n * vals[1].n)
    if opr == "/" and len(vals) == 2:
        return VALint(vals[0].n // vals[1].n)
    if opr == "%" and len(vals) == 2:
        return VALint(vals[0].n % vals[1].n)
    if opr == "<" and len(vals) == 2:
        return VALbtf(vals[0].n < vals[1].n)
    if opr == ">" and len(vals) == 2:
        return VALbtf(vals[0].n > vals[1].n)
    if opr == "<=" and len(vals) == 2:
        return VALbtf(vals[0].n <= vals[1].n)
    if opr == ">=" and len(vals) == 2:
        return VALbtf(vals[0].n >= vals[1].n)
    if opr == "=" and len(vals) == 2:
        if isinstance(vals[0], VALint) and isinstance(vals[1], VALint):
            return VALbtf(vals[0].n == vals[1].n)
        if isinstance(vals[0], VALbtf) and isinstance(vals[1], VALbtf):
            return VALbtf(vals[0].b == vals[1].b)
        if isinstance(vals[0], VALstr) and isinstance(vals[1], VALstr):
            return VALbtf(vals[0].s == vals[1].s)
        return VALbtf(False)
    if opr == "!=" and len(vals) == 2:
        if isinstance(vals[0], VALint) and isinstance(vals[1], VALint):
            return VALbtf(vals[0].n != vals[1].n)
        if isinstance(vals[0], VALbtf) and isinstance(vals[1], VALbtf):
            return VALbtf(vals[0].b != vals[1].b)
        if isinstance(vals[0], VALstr) and isinstance(vals[1], VALstr):
            return VALbtf(vals[0].s != vals[1].s)
        return VALbtf(True)
    if opr == "and" and len(vals) == 2:
        return VALbtf(vals[0].b and vals[1].b)
    if opr == "or" and len(vals) == 2:
        return VALbtf(vals[0].b or vals[1].b)
    if opr == "not" and len(vals) == 1:
        return VALbtf(not vals[0].b)
    if opr == "abs" and len(vals) == 1:
        return VALint(abs(vals[0].n))
    if opr == "print" and len(vals) == 1:
        v = vals[0]
        if isinstance(v, VALstr):
            print(v.s, end="")
        elif isinstance(v, VALint):
            print(v.n, end="")
        elif isinstance(v, VALbtf):
            print("true" if v.b else "false", end="")
        else:
            print(v, end="")
        return VALint(0)
    if opr == "string_append" and len(vals) == 2:
        return VALstr(vals[0].s + vals[1].s)
    if opr == "int_to_string" and len(vals) == 1:
        return VALstr(str(vals[0].n))
    raise RuntimeError(f"Unknown operator: {opr} with {len(vals)} args")


############################################################
# 4-2: eight-queens puzzle in LAMBDA
#
# translated from the ATS version.
# board = nested pairs: (((x0,x1),(x2,x3)),((x4,x5),(x6,x7)))
# TMfix only takes one arg so multi-arg recursive fns
# pack args into tuples.
############################################################

def eight_queens_in_lambda():

    print_dots = TMfix("print_dots", "i",
        TMif0(
            TMopr(">", [TMvar("i"), TMint(0)]),
            TMlet("_", TMopr("print", [TMstr(". ")]),
                TMapp(TMvar("print_dots"), TMopr("-", [TMvar("i"), TMint(1)]))),
            TMint(0)
        )
    )

    print_row = TMlam("i",
        TMlet("_", TMapp(TMvar("print_dots_f"), TMvar("i")),
        TMlet("_", TMopr("print", [TMstr("Q ")]),
        TMlet("_", TMapp(TMvar("print_dots_f"),
                         TMopr("-", [TMopr("-", [TMint(8), TMvar("i")]), TMint(1)])),
        TMopr("print", [TMstr("\n")]))))
    )

    # if-chain over the nested pair structure
    board_get = TMlam("bd", TMlam("i",
        TMif0(TMopr("=", [TMvar("i"), TMint(0)]),
            TMfst(TMfst(TMfst(TMvar("bd")))),
        TMif0(TMopr("=", [TMvar("i"), TMint(1)]),
            TMsnd(TMfst(TMfst(TMvar("bd")))),
        TMif0(TMopr("=", [TMvar("i"), TMint(2)]),
            TMfst(TMsnd(TMfst(TMvar("bd")))),
        TMif0(TMopr("=", [TMvar("i"), TMint(3)]),
            TMsnd(TMsnd(TMfst(TMvar("bd")))),
        TMif0(TMopr("=", [TMvar("i"), TMint(4)]),
            TMfst(TMfst(TMsnd(TMvar("bd")))),
        TMif0(TMopr("=", [TMvar("i"), TMint(5)]),
            TMsnd(TMfst(TMsnd(TMvar("bd")))),
        TMif0(TMopr("=", [TMvar("i"), TMint(6)]),
            TMfst(TMsnd(TMsnd(TMvar("bd")))),
        TMif0(TMopr("=", [TMvar("i"), TMint(7)]),
            TMsnd(TMsnd(TMsnd(TMvar("bd")))),
            TMint(-1)
        ))))))))
    ))

    # destructure, conditionally replace the i-th slot, rebuild
    board_set = TMlam("bd", TMlam("i", TMlam("j",
        TMlet("x0", TMfst(TMfst(TMfst(TMvar("bd")))),
        TMlet("x1", TMsnd(TMfst(TMfst(TMvar("bd")))),
        TMlet("x2", TMfst(TMsnd(TMfst(TMvar("bd")))),
        TMlet("x3", TMsnd(TMsnd(TMfst(TMvar("bd")))),
        TMlet("x4", TMfst(TMfst(TMsnd(TMvar("bd")))),
        TMlet("x5", TMsnd(TMfst(TMsnd(TMvar("bd")))),
        TMlet("x6", TMfst(TMsnd(TMsnd(TMvar("bd")))),
        TMlet("x7", TMsnd(TMsnd(TMsnd(TMvar("bd")))),
            TMlet("v0", TMif0(TMopr("=", [TMvar("i"), TMint(0)]), TMvar("j"), TMvar("x0")),
            TMlet("v1", TMif0(TMopr("=", [TMvar("i"), TMint(1)]), TMvar("j"), TMvar("x1")),
            TMlet("v2", TMif0(TMopr("=", [TMvar("i"), TMint(2)]), TMvar("j"), TMvar("x2")),
            TMlet("v3", TMif0(TMopr("=", [TMvar("i"), TMint(3)]), TMvar("j"), TMvar("x3")),
            TMlet("v4", TMif0(TMopr("=", [TMvar("i"), TMint(4)]), TMvar("j"), TMvar("x4")),
            TMlet("v5", TMif0(TMopr("=", [TMvar("i"), TMint(5)]), TMvar("j"), TMvar("x5")),
            TMlet("v6", TMif0(TMopr("=", [TMvar("i"), TMint(6)]), TMvar("j"), TMvar("x6")),
            TMlet("v7", TMif0(TMopr("=", [TMvar("i"), TMint(7)]), TMvar("j"), TMvar("x7")),
                TMtup(TMtup(TMtup(TMvar("v0"), TMvar("v1")),
                            TMtup(TMvar("v2"), TMvar("v3"))),
                      TMtup(TMtup(TMvar("v4"), TMvar("v5")),
                            TMtup(TMvar("v6"), TMvar("v7"))))
            ))))))))
        ))))))))
    )))

    print_board = TMlam("bd",
        TMlet("_", TMapp(TMvar("print_row_f"),
                         TMapp(TMapp(TMvar("board_get_f"), TMvar("bd")), TMint(0))),
        TMlet("_", TMapp(TMvar("print_row_f"),
                         TMapp(TMapp(TMvar("board_get_f"), TMvar("bd")), TMint(1))),
        TMlet("_", TMapp(TMvar("print_row_f"),
                         TMapp(TMapp(TMvar("board_get_f"), TMvar("bd")), TMint(2))),
        TMlet("_", TMapp(TMvar("print_row_f"),
                         TMapp(TMapp(TMvar("board_get_f"), TMvar("bd")), TMint(3))),
        TMlet("_", TMapp(TMvar("print_row_f"),
                         TMapp(TMapp(TMvar("board_get_f"), TMvar("bd")), TMint(4))),
        TMlet("_", TMapp(TMvar("print_row_f"),
                         TMapp(TMapp(TMvar("board_get_f"), TMvar("bd")), TMint(5))),
        TMlet("_", TMapp(TMvar("print_row_f"),
                         TMapp(TMapp(TMvar("board_get_f"), TMvar("bd")), TMint(6))),
        TMlet("_", TMapp(TMvar("print_row_f"),
                         TMapp(TMapp(TMvar("board_get_f"), TMvar("bd")), TMint(7))),
        TMopr("print", [TMstr("\n")])
        ))))))))
    )

    # j0 != j1 and abs(i0-i1) != abs(j0-j1)
    safety_test1 = TMlam("i0", TMlam("j0", TMlam("i1", TMlam("j1",
        TMif0(
            TMopr("!=", [TMvar("j0"), TMvar("j1")]),
            TMopr("!=", [
                TMopr("abs", [TMopr("-", [TMvar("i0"), TMvar("i1")])]),
                TMopr("abs", [TMopr("-", [TMvar("j0"), TMvar("j1")])])
            ]),
            TMbtf(False)
        )
    ))))

    # check (i0,j0) against all placed queens on rows 0..i
    # args = (i0, (j0, (bd, i)))
    safety_test2 = TMfix("safety_test2", "args",
        TMlet("i0", TMfst(TMvar("args")),
        TMlet("j0", TMfst(TMsnd(TMvar("args"))),
        TMlet("bd", TMfst(TMsnd(TMsnd(TMvar("args")))),
        TMlet("i", TMsnd(TMsnd(TMsnd(TMvar("args")))),
            TMif0(TMopr(">=", [TMvar("i"), TMint(0)]),
                TMif0(
                    TMapp(TMapp(TMapp(TMapp(
                        TMvar("safety_test1_f"),
                        TMvar("i0")), TMvar("j0")),
                        TMvar("i")),
                        TMapp(TMapp(TMvar("board_get_f"), TMvar("bd")), TMvar("i"))),
                    TMapp(TMvar("safety_test2"),
                        TMtup(TMvar("i0"),
                        TMtup(TMvar("j0"),
                        TMtup(TMvar("bd"),
                              TMopr("-", [TMvar("i"), TMint(1)]))))),
                    TMbtf(False)
                ),
                TMbtf(True)
            )
        ))))
    )

    # DFS search: args = (bd, (i, (j, nsol)))
    search = TMfix("search", "args",
        TMlet("bd", TMfst(TMvar("args")),
        TMlet("i", TMfst(TMsnd(TMvar("args"))),
        TMlet("j", TMfst(TMsnd(TMsnd(TMvar("args")))),
        TMlet("nsol", TMsnd(TMsnd(TMsnd(TMvar("args")))),
            TMif0(TMopr("<", [TMvar("j"), TMint(8)]),
                # j < N
                TMlet("test",
                    TMapp(TMvar("safety_test2_f"),
                        TMtup(TMvar("i"),
                        TMtup(TMvar("j"),
                        TMtup(TMvar("bd"),
                              TMopr("-", [TMvar("i"), TMint(1)]))))),
                    TMif0(TMvar("test"),
                        TMlet("bd1",
                            TMapp(TMapp(TMapp(TMvar("board_set_f"),
                                TMvar("bd")), TMvar("i")), TMvar("j")),
                            TMif0(TMopr("=", [TMopr("+", [TMvar("i"), TMint(1)]), TMint(8)]),
                                # found solution
                                TMlet("_", TMopr("print", [TMstr("Solution #")]),
                                TMlet("_", TMopr("print", [TMopr("+", [TMvar("nsol"), TMint(1)])]),
                                TMlet("_", TMopr("print", [TMstr(":\n\n")]),
                                TMlet("_", TMapp(TMvar("print_board_f"), TMvar("bd1")),
                                    TMapp(TMvar("search"),
                                        TMtup(TMvar("bd"),
                                        TMtup(TMvar("i"),
                                        TMtup(TMopr("+", [TMvar("j"), TMint(1)]),
                                              TMopr("+", [TMvar("nsol"), TMint(1)])))))
                                )))),
                                # not last row, go deeper
                                TMapp(TMvar("search"),
                                    TMtup(TMvar("bd1"),
                                    TMtup(TMopr("+", [TMvar("i"), TMint(1)]),
                                    TMtup(TMint(0),
                                          TMvar("nsol")))))
                            )
                        ),
                        # not safe, next column
                        TMapp(TMvar("search"),
                            TMtup(TMvar("bd"),
                            TMtup(TMvar("i"),
                            TMtup(TMopr("+", [TMvar("j"), TMint(1)]),
                                  TMvar("nsol")))))
                    )
                ),
                # j >= N, backtrack
                TMif0(TMopr(">", [TMvar("i"), TMint(0)]),
                    TMlet("prev_j",
                        TMapp(TMapp(TMvar("board_get_f"), TMvar("bd")),
                              TMopr("-", [TMvar("i"), TMint(1)])),
                        TMapp(TMvar("search"),
                            TMtup(TMvar("bd"),
                            TMtup(TMopr("-", [TMvar("i"), TMint(1)]),
                            TMtup(TMopr("+", [TMvar("prev_j"), TMint(1)]),
                                  TMvar("nsol")))))
                    ),
                    TMvar("nsol")
                )
            )
        ))))
    )

    init_board = TMtup(
        TMtup(TMtup(TMint(0), TMint(0)), TMtup(TMint(0), TMint(0))),
        TMtup(TMtup(TMint(0), TMint(0)), TMtup(TMint(0), TMint(0)))
    )

    program = \
        TMlet("print_dots_f", print_dots,
        TMlet("print_row_f", print_row,
        TMlet("board_get_f", board_get,
        TMlet("board_set_f", board_set,
        TMlet("print_board_f", print_board,
        TMlet("safety_test1_f", safety_test1,
        TMlet("safety_test2_f", safety_test2,
        TMlet("search_f", search,
            TMapp(TMvar("search_f"),
                TMtup(init_board,
                TMtup(TMint(0),
                TMtup(TMint(0),
                      TMint(0)))))
        ))))))))

    return program


############################################################
# testing
############################################################

def test_evaluator():
    print("=== Testing Evaluator ===\n")

    r = lambda_eval(TMint(42))
    assert r.n == 42
    print(f"TMint(42) => {r}")

    r = lambda_eval(TMbtf(True))
    assert r.b == True
    print(f"TMbtf(True) => {r}")

    r = lambda_eval(TMstr("hello"))
    assert r.s == "hello"
    print(f'TMstr("hello") => {r}')

    r = lambda_eval(TMapp(TMlam("x", TMvar("x")), TMint(99)))
    assert r.n == 99
    print(f"(lam x. x)(99) => {r}")

    r = lambda_eval(TMopr("+", [TMint(3), TMint(4)]))
    assert r.n == 7
    print(f"3 + 4 => {r}")

    r = lambda_eval(TMopr("<", [TMint(3), TMint(4)]))
    assert r.b == True
    print(f"3 < 4 => {r}")

    r = lambda_eval(TMif0(TMbtf(True), TMint(1), TMint(2)))
    assert r.n == 1
    print(f"if true then 1 else 2 => {r}")

    r = lambda_eval(TMfst(TMtup(TMint(10), TMint(20))))
    assert r.n == 10
    print(f"fst(10, 20) => {r}")

    r = lambda_eval(TMsnd(TMtup(TMint(10), TMint(20))))
    assert r.n == 20
    print(f"snd(10, 20) => {r}")

    r = lambda_eval(TMlet("x", TMint(5), TMopr("*", [TMvar("x"), TMvar("x")])))
    assert r.n == 25
    print(f"let x = 5 in x*x => {r}")

    factorial = TMfix("fact", "n",
        TMif0(TMopr("=", [TMvar("n"), TMint(0)]),
            TMint(1),
            TMopr("*", [TMvar("n"),
                        TMapp(TMvar("fact"), TMopr("-", [TMvar("n"), TMint(1)]))])))
    r = lambda_eval(TMapp(factorial, TMint(5)))
    assert r.n == 120
    print(f"fact(5) => {r}")

    sum_to = TMfix("sum_to", "args",
        TMlet("n", TMfst(TMvar("args")),
        TMlet("acc", TMsnd(TMvar("args")),
            TMif0(TMopr("=", [TMvar("n"), TMint(0)]),
                TMvar("acc"),
                TMapp(TMvar("sum_to"),
                    TMtup(TMopr("-", [TMvar("n"), TMint(1)]),
                          TMopr("+", [TMvar("acc"), TMvar("n")])))
            )
        ))
    )
    r = lambda_eval(TMapp(sum_to, TMtup(TMint(10), TMint(0))))
    assert r.n == 55
    print(f"sum_to(10, 0) => {r}")

    print("\nAll evaluator tests passed.\n")


def test_eight_queens():
    print("=== Running 8-Queens Puzzle ===\n")
    program = eight_queens_in_lambda()
    result = lambda_eval(program)
    print(f"\nTotal solutions: {result}")
    if isinstance(result, VALint):
        assert result.n == 92, f"Expected 92 solutions, got {result.n}"
        print("Correct: 92 solutions found.")


if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(100000)
    test_evaluator()
    test_eight_queens()

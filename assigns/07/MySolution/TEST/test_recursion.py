"""
Test: Recursive functions using DEfix and DEfix1 (factorial)
Expected: Type checks pass, JS output computes factorial correctly
"""
from a7 import *

print("=== test_recursion: Fix / Factorial ===")

var_f = dexp_var("f")
var_n = dexp_var("n")
var_i = dexp_var("i")
var_r = dexp_var("r")

# Typed factorial: fix f(n:int):int = if n<=0 then 1 else n * f(n-1)
e_fact1 = dexp_fix1("f", "n", styp_int,
    dexp_if0(DE_lte(var_n, dexp_int(0)),
        dexp_int(1),
        DE_mul(var_n, dexp_app(var_f, DE_sub(var_n, dexp_int(1))))),
    styp_int)
print("tinfer(fact_typed) = " + str(dexp_tinfer(e_fact1)))  # int -> int

# Untyped factorial: fix f(n) = if n<=0 then 1 else n * f(n-1)
e_fact = dexp_fix("f", "n",
    dexp_if0(DE_lte(var_n, dexp_int(0)),
        dexp_int(1),
        DE_mul(var_n, dexp_app(var_f, DE_sub(var_n, dexp_int(1))))))
print("tinfer(fact_untyped) = " + str(dexp_tinfer(e_fact)))  # int -> int

# Tail-recursive factorial using accumulator
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
print("tinfer(fact_tailrec) = " + str(dexp_tinfer(e_fact2)))  # int -> int

# JS output
js = ""
js += "// fact(10) => 3628800\n"
js += "console.log((" + dexp_trx2js(e_fact) + ")(10));\n"
js += "// fact_typed(10) => 3628800\n"
js += "console.log((" + dexp_trx2js(e_fact1) + ")(10));\n"
js += "// fact_tailrec(10) => 3628800\n"
js += "console.log((" + dexp_trx2js(e_fact2) + ")(10));\n"
print(js)

with open("TEST/test_recursion.js", "w") as f:
    f.write(js)
print("Written to TEST/test_recursion.js")

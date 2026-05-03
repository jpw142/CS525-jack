"""
Test: Lambda (typed and untyped), application, let-binding, if-then-else
Expected: Type checks pass, JS output runs correctly in Node.js
"""
from a7 import *

print("=== test_lambda: Lambda, App, Let, If ===")

var_x = dexp_var("x")

# Typed lambda: lam(x:int). x + x
e_dbl = dexp_lam1("x", styp_int, DE_add(var_x, var_x))
print("tinfer(lam x:int. x+x) = " + str(dexp_tinfer(e_dbl)))  # int -> int

# Untyped lambda: lam(x). x + x (should infer int -> int)
e_dbl2 = dexp_lam("x", DE_add(var_x, var_x))
print("tinfer(lam x. x+x) = " + str(dexp_tinfer(e_dbl2)))  # int -> int

# Application: (lam x. x+x)(5)
e_app = dexp_app(e_dbl2, dexp_int(5))
print("tinfer(dbl(5)) = " + str(dexp_tinfer(e_app)))  # int

# Identity: lam(x). x (polymorphic)
e_id = dexp_lam("x", dexp_var("x"))
print("tinfer(id) = " + str(dexp_tinfer(e_id)))  # ?->?

# If-then-else
e_if = dexp_if0(dexp_btf(True), dexp_int(1), dexp_int(2))
print("tinfer(if true then 1 else 2) = " + str(dexp_tinfer(e_if)))  # int

# Let-binding: let x = 42 in x + 1
e_let = dexp_let("x", dexp_int(42), DE_add(dexp_var("x"), dexp_int(1)))
print("tinfer(let x=42 in x+1) = " + str(dexp_tinfer(e_let)))  # int

# JS output
print("\n--- JS Output ---")
js = ""
js += "// (lam x. x+x)(5) => 10\n"
js += "console.log(" + dexp_trx2js(e_app) + ");\n"
js += "// if true then 1 else 2 => 1\n"
js += "console.log(" + dexp_trx2js(e_if) + ");\n"
js += "// let x = 42 in x + 1 => 43\n"
js += "console.log(" + dexp_trx2js(e_let) + ");\n"
print(js)

with open("TEST/test_lambda.js", "w") as f:
    f.write(js)
print("Written to TEST/test_lambda.js")

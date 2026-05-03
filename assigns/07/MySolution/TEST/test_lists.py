"""
Test: Lists (nil, cons, head, tail, length)
Expected: Type checks pass, JS output runs correctly
"""
from a7 import *

print("=== test_lists: List operations ===")

# Empty list
e_nil = dexp_list_nil()
print("tinfer(nil) = " + str(dexp_tinfer(e_nil)))  # list(?)

# cons(1, nil) => [1]
e_cons1 = dexp_list_cons(dexp_int(1), dexp_list_nil())
print("tinfer(cons(1,nil)) = " + str(dexp_tinfer(e_cons1)))  # list(int)

# cons(1, cons(2, cons(3, nil))) => [1,2,3]
e_list = dexp_list_cons(dexp_int(1),
            dexp_list_cons(dexp_int(2),
                dexp_list_cons(dexp_int(3), dexp_list_nil())))
print("tinfer([1,2,3]) = " + str(dexp_tinfer(e_list)))  # list(int)

# list_head([1,2,3])
e_hd = dexp_opr("list_head", [e_list])
print("tinfer(head([1,2,3])) = " + str(dexp_tinfer(e_hd)))  # int

# list_tail([1,2,3])
e_tl = dexp_opr("list_tail", [e_list])
print("tinfer(tail([1,2,3])) = " + str(dexp_tinfer(e_tl)))  # list(int)

# list_length([1,2,3])
e_len = dexp_opr("list_length", [e_list])
print("tinfer(length([1,2,3])) = " + str(dexp_tinfer(e_len)))  # int

# Recursive sum over a list using fix
# sum = fix f(xs) = if length(xs) = 0 then 0 else head(xs) + f(tail(xs))
var_f = dexp_var("f")
var_xs = dexp_var("xs")
e_sum = dexp_fix("f", "xs",
    dexp_if0(
        DE_eq(dexp_opr("list_length", [var_xs]), dexp_int(0)),
        dexp_int(0),
        DE_add(
            dexp_opr("list_head", [var_xs]),
            dexp_app(var_f, dexp_opr("list_tail", [var_xs])))))
print("tinfer(list_sum) = " + str(dexp_tinfer(e_sum)))  # list(int) -> int

# JS output
js = ""
js += "// [1,2,3]\n"
js += "console.log(" + dexp_trx2js(e_list) + ");\n"
js += "// head([1,2,3]) => 1\n"
js += "console.log(" + dexp_trx2js(e_hd) + ");\n"
js += "// tail([1,2,3]) => [2,3]\n"
js += "console.log(" + dexp_trx2js(e_tl) + ");\n"
js += "// length([1,2,3]) => 3\n"
js += "console.log(" + dexp_trx2js(e_len) + ");\n"
js += "// sum([1,2,3]) => 6\n"
js += "console.log((" + dexp_trx2js(e_sum) + ")(" + dexp_trx2js(e_list) + "));\n"
print(js)

with open("TEST/test_lists.js", "w") as f:
    f.write(js)
print("Written to TEST/test_lists.js")

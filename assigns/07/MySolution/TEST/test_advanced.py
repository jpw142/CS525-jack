"""
Test: Arrays, lazy evaluation, streams, type annotations, higher-order functions
Expected: Type checks pass, JS output runs correctly
"""
from a7 import *

print("=== test_advanced: Arrays, Lazy, Streams, Anno, Higher-Order ===")

# --- Arrays ---
# array_size_val(5, 0) => [0,0,0,0,0]
e_arry_v = dexp_arry_size_val(dexp_int(5), dexp_int(0))
print("tinfer(array(5,0)) = " + str(dexp_tinfer(e_arry_v)))  # arry(int)

# array_size_fun(5, lam i. i*i) => [0,1,4,9,16]
e_arry_f = dexp_arry_size_fun(dexp_int(5), dexp_lam("i", DE_mul(dexp_var("i"), dexp_var("i"))))
print("tinfer(array(5, i->i*i)) = " + str(dexp_tinfer(e_arry_f)))  # arry(int)

# --- Lazy ---
e_lazy = dexp_lazy(dexp_int(42))
print("tinfer(lazy(42)) = " + str(dexp_tinfer(e_lazy)))  # lazy(int)

# force(lazy(42))
e_force = dexp_opr("lazy_force", [e_lazy])
print("tinfer(force(lazy(42))) = " + str(dexp_tinfer(e_force)))  # int

# --- Streams ---
e_stcn_nil = dexp_stcn_nil()
print("tinfer(stcn_nil) = " + str(dexp_tinfer(e_stcn_nil)))  # stcn(?)

e_stcn = dexp_stcn_cons(dexp_int(1), dexp_lazy(dexp_stcn_nil()))
print("tinfer(stcn_cons(1, lazy(nil))) = " + str(dexp_tinfer(e_stcn)))  # stcn(int)

# --- Type annotation ---
e_anno = dexp_anno(dexp_int(42), styp_int)
print("tinfer(anno(42, int)) = " + str(dexp_tinfer(e_anno)))  # int

# --- Higher-order: Church numeral 3 ---
styp_fun_int_int = styp_fun(styp_int, styp_int)
var_f = dexp_var("f")
e_ch3 = dexp_lam1("f", styp_fun_int_int,
    dexp_lam1("x", styp_int,
        dexp_app(var_f,
            dexp_app(var_f,
                dexp_app(var_f, dexp_var("x"))))))
print("tinfer(church3) = " + str(dexp_tinfer(e_ch3)))  # (int->int) -> int -> int

# --- Higher-order: map over list ---
# map = fix map(f) = lam(xs). if length(xs) = 0 then nil else cons(f(head(xs)), map(f)(tail(xs)))
var_map = dexp_var("map")
var_xs = dexp_var("xs")
e_map = dexp_fix("map", "f",
    dexp_lam("xs",
        dexp_if0(
            DE_eq(dexp_opr("list_length", [var_xs]), dexp_int(0)),
            dexp_list_nil(),
            dexp_list_cons(
                dexp_app(var_f, dexp_opr("list_head", [var_xs])),
                dexp_app(dexp_app(var_map, var_f), dexp_opr("list_tail", [var_xs]))))))
print("tinfer(map) = " + str(dexp_tinfer(e_map)))

# JS output
js = ""
js += "// array(5, 0) => [0,0,0,0,0]\n"
js += "console.log(" + dexp_trx2js(e_arry_v) + ");\n"
js += "// array(5, i->i*i) => [0,1,4,9,16]\n"
js += "console.log(" + dexp_trx2js(e_arry_f) + ");\n"
js += "// force(lazy(42)) => 42\n"
js += "console.log(" + dexp_trx2js(e_force) + ");\n"
js += "// stream cons\n"
js += "console.log(" + dexp_trx2js(e_stcn) + ");\n"
js += "// church3(x=>x+1)(0) => 3\n"
js += "console.log((" + dexp_trx2js(e_ch3) + ")(function(x){return x+1;})(0));\n"
e_list123 = dexp_list_cons(dexp_int(1), dexp_list_cons(dexp_int(2), dexp_list_cons(dexp_int(3), dexp_list_nil())))
js += "// map(x=>x*10, [1,2,3]) => [10,20,30]\n"
js += "console.log((" + dexp_trx2js(e_map) + ")(function(x){return x*10;})(" + dexp_trx2js(e_list123) + "));\n"
print(js)

with open("TEST/test_advanced.js", "w") as f:
    f.write(js)
print("Written to TEST/test_advanced.js")

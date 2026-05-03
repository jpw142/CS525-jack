"""
Test: Tuples, fst, snd projections
Expected: Type checks pass, JS output runs correctly in Node.js
"""
from a7 import *

print("=== test_tuples: Tuples, Fst, Snd ===")

# Tuple of (int, bool)
e_tup = dexp_tup(dexp_int(1), dexp_btf(True))
print("tinfer((1, true)) = " + str(dexp_tinfer(e_tup)))  # (int, bool)

# Fst
e_fst = dexp_fst(e_tup)
print("tinfer(fst(1, true)) = " + str(dexp_tinfer(e_fst)))  # int

# Snd
e_snd = dexp_snd(e_tup)
print("tinfer(snd(1, true)) = " + str(dexp_tinfer(e_snd)))  # bool

# Nested tuple: ((1, 2), (3, 4))
e_nested = dexp_tup(dexp_tup(dexp_int(1), dexp_int(2)),
                    dexp_tup(dexp_int(3), dexp_int(4)))
e_deep = dexp_fst(dexp_snd(e_nested))  # should be 3
print("tinfer(fst(snd((1,2),(3,4)))) = " + str(dexp_tinfer(e_deep)))  # int

# JS output
js = ""
js += "// (1, true) => [1, true]\n"
js += "console.log(" + dexp_trx2js(e_tup) + ");\n"
js += "// fst(1, true) => 1\n"
js += "console.log(" + dexp_trx2js(e_fst) + ");\n"
js += "// snd(1, true) => true\n"
js += "console.log(" + dexp_trx2js(e_snd) + ");\n"
js += "// fst(snd((1,2),(3,4))) => 3\n"
js += "console.log(" + dexp_trx2js(e_deep) + ");\n"
print(js)

with open("TEST/test_tuples.js", "w") as f:
    f.write(js)
print("Written to TEST/test_tuples.js")

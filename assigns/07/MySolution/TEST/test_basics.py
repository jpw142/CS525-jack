"""
Test: Basic literals (int, bool, string) and arithmetic operators
Expected: Type checks pass, JS output runs correctly in Node.js
"""
from a7 import *

print("=== test_basics: Literals and Arithmetic ===")

# Integer literal
e1 = dexp_int(42)
t1 = dexp_tinfer(e1)
print("tinfer(42) = " + str(t1))  # STbas(int)

# Boolean literal
e2 = dexp_btf(True)
t2 = dexp_tinfer(e2)
print("tinfer(true) = " + str(t2))  # STbas(bool)

# String literal
e3 = dexp_str("hello")
t3 = dexp_tinfer(e3)
print("tinfer(\"hello\") = " + str(t3))  # STbas(string)

# Addition: 1 + 2
e4 = DE_add(dexp_int(1), dexp_int(2))
t4 = dexp_tinfer(e4)
print("tinfer(1+2) = " + str(t4))  # STbas(int)

# Comparison: 1 <= 2
e5 = DE_lte(dexp_int(1), dexp_int(2))
t5 = dexp_tinfer(e5)
print("tinfer(1<=2) = " + str(t5))  # STbas(bool)

# JS output
print("\n--- JS Output ---")
print("console.log(" + dexp_trx2js(e1) + ");")
print("console.log(" + dexp_trx2js(e2) + ");")
print("console.log(" + dexp_trx2js(e3) + ");")
print("console.log(" + dexp_trx2js(e4) + ");")
print("console.log(" + dexp_trx2js(e5) + ");")

# Write runnable JS
js = ""
js += "console.log(" + dexp_trx2js(e1) + ");\n"
js += "console.log(" + dexp_trx2js(e2) + ");\n"
js += "console.log(" + dexp_trx2js(e3) + ");\n"
js += "console.log(" + dexp_trx2js(e4) + ");\n"
js += "console.log(" + dexp_trx2js(e5) + ");\n"
with open("TEST/test_basics.js", "w") as f:
    f.write(js)
print("\nWritten to TEST/test_basics.js")

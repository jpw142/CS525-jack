import sys
import os

import sys
sys.path.insert(0, '../../02/MySolution')

from lambda0 import (
    TMvar, TMlam, TMapp,
    term_freevars, term_freshvar, term_subst0, term_gsubst
)

#
############################################################
############################################################
#
# Assign03 for CS525, Spring, 2026
# It is due the 10th of February, 2026
# Note that the due time is always 11:59pm of
# the due date unless specified otherwise.
#
############################################################
############################################################

def lambda_normalize(tm0):
    """
    Leftmost evaluation strategy with normalization under lambda.
    """
    if tm0.ctag == "TMvar":
        return tm0
    
    if tm0.ctag == "TMapp":
        # Check if this is a redex: (λx.M) N
        if tm0.arg1.ctag == "TMlam":
            # Beta reduction: substitute N for x in M
            x = tm0.arg1.arg1
            body = tm0.arg1.arg2
            arg = tm0.arg2
            reduced = term_gsubst(body, x, arg)
            # Continue normalizing the result (important!)
            return lambda_normalize(reduced)
        else:
            # Not a redex yet - normalize the function part first (leftmost!)
            fn_norm = lambda_normalize(tm0.arg1)
            # After normalizing, check if it became a lambda
            if fn_norm.ctag == "TMlam":
                # Now it's a redex - reduce it
                x = fn_norm.arg1
                body = fn_norm.arg2
                arg = tm0.arg2
                reduced = term_gsubst(body, x, arg)
                return lambda_normalize(reduced)
            else:
                # Normalize the argument too
                arg_norm = lambda_normalize(tm0.arg2)
                return TMapp(fn_norm, arg_norm)
    
    if tm0.ctag == "TMlam":
        body_norm = lambda_normalize(tm0.arg2)
        return TMlam(tm0.arg1, body_norm)
    
    raise TypeError(tm0)

def ipred_in_lambda():
    """
    Predecessor function: pred n returns n-1 (or 0 if n=0)
    Formula: pred = λn.λf.λx.n (λg.λh.h (g f)) (λu.x) (λu.u)
    """
    n = TMvar("n")
    f = TMvar("f")
    x = TMvar("x")
    g = TMvar("g")
    h = TMvar("h")
    u = TMvar("u")
    
    # λg.λh.h (g f) - the "shifting" function
    shift = TMlam("g", TMlam("h", TMapp(h, TMapp(g, f))))
    
    # λu.x - constant function returning x
    const_x = TMlam("u", x)
    
    # λu.u - identity function
    identity = TMlam("u", u)
    
    # Build: n shift const_x identity
    body = TMapp(TMapp(TMapp(n, shift), const_x), identity)
    
    # Wrap in λn.λf.λx
    return TMlam("n", TMlam("f", TMlam("x", body)))

def isqrt_in_lambda():
    """
    Simple iterative square root
    """
    zero = TMlam("f", TMlam("x", TMvar("x")))
    one = TMlam("f", TMlam("x", TMapp(TMvar("f"), TMvar("x"))))
    two = TMlam("f", TMlam("x", TMapp(TMvar("f"), TMapp(TMvar("f"), TMvar("x")))))
    
    pair = TMlam("x", TMlam("y", TMlam("f", TMapp(TMapp(TMvar("f"), TMvar("x")), TMvar("y")))))
    triple = TMlam("x", TMlam("y", TMlam("z", TMapp(TMapp(pair, TMvar("x")), TMapp(TMapp(pair, TMvar("y")), TMvar("z"))))))
    fst = TMlam("p", TMapp(TMvar("p"), TMlam("x", TMlam("y", TMvar("x")))))
    snd = TMlam("p", TMapp(TMvar("p"), TMlam("x", TMlam("y", TMvar("y")))))
    
    succ = TMlam("n", TMlam("f", TMlam("x", TMapp(TMvar("f"), TMapp(TMapp(TMvar("n"), TMvar("f")), TMvar("x"))))))
    add = TMlam("m", TMlam("n", TMlam("f", TMlam("x", TMapp(TMapp(TMvar("m"), TMvar("f")), TMapp(TMapp(TMvar("n"), TMvar("f")), TMvar("x")))))))
    
    pred = TMlam("n", TMlam("f", TMlam("x",
        TMapp(TMapp(TMapp(TMvar("n"), TMlam("g", TMlam("h", TMapp(TMvar("h"), TMapp(TMvar("g"), TMvar("f")))))),
            TMlam("u", TMvar("x"))), TMlam("u", TMvar("u"))))))
    sub = TMlam("m", TMlam("n", TMapp(TMapp(TMvar("n"), pred), TMvar("m"))))
    
    true_c = TMlam("x", TMlam("y", TMvar("x")))
    false_c = TMlam("x", TMlam("y", TMvar("y")))
    iszero = TMlam("n", TMapp(TMapp(TMvar("n"), TMlam("x", false_c)), true_c))
    leq = TMlam("m", TMlam("n", TMapp(iszero, TMapp(TMapp(sub, TMvar("m")), TMvar("n")))))
    if_c = TMlam("c", TMlam("t", TMlam("e", TMapp(TMapp(TMvar("c"), TMvar("t")), TMvar("e")))))
    
    n_var = TMvar("n")
    state_var = TMvar("state")
    get_i = TMapp(fst, state_var)
    get_isq = TMapp(fst, TMapp(snd, state_var))
    get_inc = TMapp(snd, TMapp(snd, state_var))
    
    step_body = TMapp(TMapp(TMapp(if_c,
        TMapp(TMapp(leq, TMapp(TMapp(add, get_isq), get_inc)), n_var)),
        TMapp(TMapp(TMapp(triple, TMapp(succ, get_i)), TMapp(TMapp(add, get_isq), get_inc)), TMapp(TMapp(add, get_inc), two))),
        state_var)
    
    step = TMlam("n", TMlam("state", step_body))
    init_state = TMapp(TMapp(TMapp(triple, zero), zero), one)
    main_body = TMapp(fst, TMapp(TMapp(TMvar("n"), TMapp(step, TMvar("n"))), init_state))
    
    return TMlam("n", main_body)
############################################################
############################################################
# TEST SUITE
############################################################
############################################################

def church_numeral(n):
    """Convert integer n to Church numeral: λf.λx.f^n(x)"""
    f = TMvar("f")
    x = TMvar("x")
    
    # Build f(f(...f(x)...)) with n applications
    result = x
    for _ in range(n):
        result = TMapp(f, result)
    
    return TMlam("f", TMlam("x", result))

def church_to_int(tm):
    """
    Convert normalized Church numeral back to integer
    Counts the number of f applications in λf.λx.f^n(x)
    """
    normalized = lambda_normalize(tm)
    
    # Should be λf.λx.body
    if normalized.ctag != "TMlam":
        return None
    f_name = normalized.arg1
    
    if normalized.arg2.ctag != "TMlam":
        return None
    x_name = normalized.arg2.arg1
    
    body = normalized.arg2.arg2
    
    # Count applications of f
    count = 0
    current = body
    while current.ctag == "TMapp":
        if current.arg1.ctag == "TMvar" and current.arg1.arg1 == f_name:
            count += 1
            current = current.arg2
        else:
            return None
    
    # Should end with x
    if current.ctag == "TMvar" and current.arg1 == x_name:
        return count
    
    return None

def test_church_numerals():
    """Test our Church numeral conversion functions"""
    print("\n=== Testing Church Numeral Conversions ===")
    for i in range(5):
        cn = church_numeral(i)
        result = church_to_int(cn)
        print(f"church_numeral({i}) -> church_to_int = {result}")
        assert result == i, f"Failed for {i}"
    print("  Church numeral conversions working")

def test_lambda_normalize_basic():
    """Test basic normalization"""
    print("\n=== Testing lambda_normalize (Basic) ===")
    
    # Test 1: Identity applied to a variable
    # (λx.x) y -> y
    id_fn = TMlam("x", TMvar("x"))
    app = TMapp(id_fn, TMvar("y"))
    result = lambda_normalize(app)
    print(f"(λx.x) y = {result}")
    assert result.ctag == "TMvar" and result.arg1 == "y"
    print("  Identity application works")
    
    # Test 2: K combinator
    # (λx.λy.x) a b -> a
    k_fn = TMlam("x", TMlam("y", TMvar("x")))
    app1 = TMapp(k_fn, TMvar("a"))
    app2 = TMapp(app1, TMvar("b"))
    result = lambda_normalize(app2)
    print(f"K a b = {result}")
    assert result.ctag == "TMvar" and result.arg1 == "a"
    print("  K combinator works")
    
    # Test 3: Normalization under lambda
    # λz.(λx.x) z should normalize to λz.z
    inner = TMapp(id_fn, TMvar("z"))
    outer = TMlam("z", inner)
    result = lambda_normalize(outer)
    print(f"λz.(λx.x) z = {result}")
    assert result.ctag == "TMlam"
    assert result.arg2.ctag == "TMvar"
    print("  Normalization under lambda works")

def test_lambda_normalize_church():
    """Test normalization with Church numerals"""
    print("\n=== Testing lambda_normalize (Church Numerals) ===")
    
    # Successor function: λn.λf.λx.f (n f x)
    succ = TMlam("n", TMlam("f", TMlam("x",
        TMapp(TMvar("f"), 
              TMapp(TMapp(TMvar("n"), TMvar("f")), TMvar("x"))))))
    
    # Apply succ to Church numeral 0
    zero = church_numeral(0)
    app = TMapp(succ, zero)
    result = lambda_normalize(app)
    result_int = church_to_int(result)
    print(f"succ 0 = {result_int}")
    assert result_int == 1, f"Expected 1, got {result_int}"
    
    # Apply succ to Church numeral 2
    two = church_numeral(2)
    app = TMapp(succ, two)
    result = lambda_normalize(app)
    result_int = church_to_int(result)
    print(f"succ 2 = {result_int}")
    assert result_int == 3, f"Expected 3, got {result_int}"
    
    print("  Successor function works correctly")

def test_ipred():
    """Test predecessor function"""
    print("\n=== Testing ipred_in_lambda ===")
    
    pred = ipred_in_lambda()
    
    # Test pred 0 = 0
    zero = church_numeral(0)
    app = TMapp(pred, zero)
    result = lambda_normalize(app)
    result_int = church_to_int(result)
    print(f"pred 0 = {result_int}")
    assert result_int == 0, f"pred 0: expected 0, got {result_int}"
    
    # Test pred 1 = 0
    one = church_numeral(1)
    app = TMapp(pred, one)
    result = lambda_normalize(app)
    result_int = church_to_int(result)
    print(f"pred 1 = {result_int}")
    assert result_int == 0, f"pred 1: expected 0, got {result_int}"
    
    # Test pred 3 = 2
    three = church_numeral(3)
    app = TMapp(pred, three)
    result = lambda_normalize(app)
    result_int = church_to_int(result)
    print(f"pred 3 = {result_int}")
    assert result_int == 2, f"pred 3: expected 2, got {result_int}"
    
    # Test pred 5 = 4
    five = church_numeral(5)
    app = TMapp(pred, five)
    result = lambda_normalize(app)
    result_int = church_to_int(result)
    print(f"pred 5 = {result_int}")
    assert result_int == 4, f"pred 5: expected 4, got {result_int}"
    
    print("  Predecessor function works correctly")

def test_isqrt():
    """Test integer square root function"""
    print("\n=== Testing isqrt_in_lambda ===")
    
    sqrt_fn = isqrt_in_lambda()
    
    test_cases = [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 2),
    ]
    
    for n, expected in test_cases:
        cn = church_numeral(n)
        app = TMapp(sqrt_fn, cn)
        result = lambda_normalize(app)
        result_int = church_to_int(result)
        print(f"isqrt({n}) = {result_int} (expected {expected})")
        assert result_int == expected, f"isqrt({n}): expected {expected}, got {result_int}"
    print(" Square root function works correctly")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("RUNNING ALL TESTS FOR ASSIGN03")
    print("=" * 60)
    
    test_church_numerals()
    test_lambda_normalize_basic()
    test_lambda_normalize_church()
    test_ipred()
    test_isqrt()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)

run_all_tests()


############################################################
#
# Assign01 for CS525, Spring, 2026
# It is due the 27th of January, 2026
# Note that the due time is always 11:59pm of
# the due date unless is specified otherwise.
#
############################################################
# datatype term =
# | TMvar of strn
# | TMlam of (strn, term)
# | TMapp of (term, term)
############################################################
#
class term:
    ctag = ""
# end-of-class(term)
#
class term_var(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMvar"
    def __str__(self):
        return ("TMvar(" + self.arg1 + ")")
# end-of-class(term_var(term))
#
class term_lam(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMlam"
    def __str__(self):
        return ("TMlam(" + self.arg1 + "," + str(self.arg2) + ")")
# end-of-class(term_lam(term))
#
class term_app(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMapp"
    def __str__(self):
        return ("TMapp(" + str(self.arg1) + "," + str(self.arg2) + ")")
# end-of-class(term_app(term))
#
############################################################
#
def TM1var(x00):
    return term_var(x00)
def TM1lam(x00, tm1):
    return term_lam(x00, tm1)
def TM1app(tm1, tm2):
    return term_app(tm1, tm2)
#
############################################################
#
def I_():
    x = TM1var("x")
    return TM1lam("x", x)
def K_():
    x = TM1var("x")
    return TM1lam("x", TM1lam("y", x))
def S_():
    x = TM1var("x")
    y = TM1var("y")
    z = TM1var("z")
    return TM1lam("x", TM1lam("y", TM1lam("z", TM1app(TM1app(x, z), TM1app(y, z)))))
#
_ = print("I =", I_())
_ = print("K =", K_())
_ = print("S =", S_())
#
############################################################

def term_freevars(tm0):
    """
    Points: 10
    This function takes a term [tm0] and returns the set of
    free variables in [tm0]. The set returned should be the
    built-in set in Python
    """
    if tm0.ctag == "TMvar": 
        return {tm0.arg1}
    else if tm0.ctag == "TMlam":
        free = term_freevars{tm0.arg1}
        free2 = term_freevars(tm0.arg2}
        free.update(free2)
        return free
    else:
        free = term_freevars{tm0.arg2}
        free.remove(tm0.arg1)
        return free

############################################################
############################################################
# end of [HWXI/CS525-2026-Fall/assigns/01/lambda0.py]
############################################################
############################################################

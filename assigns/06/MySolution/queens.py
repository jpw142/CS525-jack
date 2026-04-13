##################################################################
# 8-Queens Puzzle encoded in dexp AST
# Transpiled to JavaScript via dexp_trx2js
##################################################################

from a6 import *

############################################################
# Shortcuts
############################################################

def V(name):       return dexp_var(name)
def I(n):          return dexp_int(n)
def B(b):          return dexp_btf(b)
def S(s):          return dexp_str(s)
def LAM(x, body):  return dexp_lam(x, body)
def APP(f, a):     return dexp_app(f, a)
def APP2(f, a, b): return dexp_app(dexp_app(f, a), b)
def APP3(f, a, b, c): return dexp_app(dexp_app(dexp_app(f, a), b), c)
def APP4(f, a, b, c, d): return dexp_app(dexp_app(dexp_app(dexp_app(f, a), b), c), d)
def OPR(op, args): return dexp_opr(op, args)
def IF0(t, th, el): return dexp_if0(t, th, el)
def LET(x, d, s): return dexp_let(x, d, s)
def FIX(f, x, body): return dexp_fix(f, x, body)
def TUP(a, b):     return dexp_tup(a, b)
def FST(e):        return dexp_fst(e)
def SND(e):        return dexp_snd(e)

def ADD(a, b): return OPR("+", [a, b])
def SUB(a, b): return OPR("-", [a, b])
def MUL(a, b): return OPR("*", [a, b])
def EQ(a, b):  return OPR("=", [a, b])
def NEQ(a, b): return OPR("!=", [a, b])
def LT(a, b):  return OPR("<", [a, b])
def LTE(a, b): return OPR("<=", [a, b])
def GT(a, b):  return OPR(">", [a, b])
def GTE(a, b): return OPR(">=", [a, b])
def STRCAT(a, b): return OPR("string_append", [a, b])
def TOSTR(a): return OPR("tostr", [a])
def PRINT(a): return OPR("print", [a])

############################################################
# Board = nested pair: (((x0,x1),(x2,x3)),((x4,x5),(x6,x7)))
############################################################

empty_board = TUP(TUP(TUP(I(-1), I(-1)), TUP(I(-1), I(-1))),
                  TUP(TUP(I(-1), I(-1)), TUP(I(-1), I(-1))))

board_get = LAM("bd", LAM("i",
    IF0(EQ(V("i"), I(0)), FST(FST(FST(V("bd")))),
    IF0(EQ(V("i"), I(1)), SND(FST(FST(V("bd")))),
    IF0(EQ(V("i"), I(2)), FST(SND(FST(V("bd")))),
    IF0(EQ(V("i"), I(3)), SND(SND(FST(V("bd")))),
    IF0(EQ(V("i"), I(4)), FST(FST(SND(V("bd")))),
    IF0(EQ(V("i"), I(5)), SND(FST(SND(V("bd")))),
    IF0(EQ(V("i"), I(6)), FST(SND(SND(V("bd")))),
    IF0(EQ(V("i"), I(7)), SND(SND(SND(V("bd")))),
        I(-1)
    ))))))))
))

board_set = LAM("bd", LAM("i", LAM("j",
    LET("x0", FST(FST(FST(V("bd")))),
    LET("x1", SND(FST(FST(V("bd")))),
    LET("x2", FST(SND(FST(V("bd")))),
    LET("x3", SND(SND(FST(V("bd")))),
    LET("x4", FST(FST(SND(V("bd")))),
    LET("x5", SND(FST(SND(V("bd")))),
    LET("x6", FST(SND(SND(V("bd")))),
    LET("x7", SND(SND(SND(V("bd")))),
        LET("v0", IF0(EQ(V("i"), I(0)), V("j"), V("x0")),
        LET("v1", IF0(EQ(V("i"), I(1)), V("j"), V("x1")),
        LET("v2", IF0(EQ(V("i"), I(2)), V("j"), V("x2")),
        LET("v3", IF0(EQ(V("i"), I(3)), V("j"), V("x3")),
        LET("v4", IF0(EQ(V("i"), I(4)), V("j"), V("x4")),
        LET("v5", IF0(EQ(V("i"), I(5)), V("j"), V("x5")),
        LET("v6", IF0(EQ(V("i"), I(6)), V("j"), V("x6")),
        LET("v7", IF0(EQ(V("i"), I(7)), V("j"), V("x7")),
            TUP(TUP(TUP(V("v0"), V("v1")),
                     TUP(V("v2"), V("v3"))),
                TUP(TUP(V("v4"), V("v5")),
                     TUP(V("v6"), V("v7"))))
        ))))))))
    ))))))))
)))

my_abs = LAM("x", IF0(LT(V("x"), I(0)), SUB(I(0), V("x")), V("x")))

safety_test1 = LAM("i0", LAM("j0", LAM("i1", LAM("j1",
    IF0(NEQ(V("j0"), V("j1")),
        NEQ(APP(V("my_abs"), SUB(V("i0"), V("i1"))),
            APP(V("my_abs"), SUB(V("j0"), V("j1")))),
        B(False))
))))

# safety_test2(bd, i0, j0, k): curried
safety_test2 = FIX("safety_test2", "bd",
    LAM("i0", LAM("j0", LAM("k",
        IF0(LTE(V("k"), I(0)),
            B(True),
            LET("k1", SUB(V("k"), I(1)),
            LET("jk", APP2(V("board_get_f"), V("bd"), V("k1")),
                IF0(APP4(V("safety_test1_f"), V("i0"), V("j0"), V("k1"), V("jk")),
                    APP4(V("safety_test2"), V("bd"), V("i0"), V("j0"), V("k1")),
                    B(False))
            ))
        )
    )))
)

############################################################
# Build a row string: "Q . . . . . . . " etc.
# build_row(col, k, acc) -> string
# Accumulates into acc, returns final string when k>=8
############################################################
build_row = FIX("build_row", "col",
    LAM("k", LAM("acc",
        IF0(GTE(V("k"), I(8)),
            V("acc"),
            IF0(EQ(V("k"), V("col")),
                APP3(V("build_row"), V("col"), ADD(V("k"), I(1)), STRCAT(V("acc"), S("Q "))),
                APP3(V("build_row"), V("col"), ADD(V("k"), I(1)), STRCAT(V("acc"), S(". ")))
            ))
    ))
)

############################################################
# print_board(bd, r): prints each row on its own line
############################################################
print_board_fn = FIX("print_board", "bd",
    LAM("r",
        IF0(GTE(V("r"), I(8)),
            I(0),
            LET("col", APP2(V("board_get_f"), V("bd"), V("r")),
            LET("line", APP3(V("build_row_f"), V("col"), I(0), S("")),
            LET("_p", PRINT(V("line")),
                APP2(V("print_board"), V("bd"), ADD(V("r"), I(1)))
            )))
        )
    )
)

############################################################
# solver(args) where args = (mode, (bd, (row, (col, nsol))))
# mode=0: solve, mode=1: try_col
############################################################
solver = FIX("solver", "args",
    LET("mode", FST(V("args")),
    LET("bd",   FST(SND(V("args"))),
    LET("row",  FST(SND(SND(V("args")))),
    LET("col",  FST(SND(SND(SND(V("args"))))),
    LET("nsol", SND(SND(SND(SND(V("args"))))),
        IF0(EQ(V("mode"), I(0)),
            # SOLVE mode
            IF0(GTE(V("row"), I(8)),
                # Found solution — print header as one line, then board
                LET("nsol1", ADD(V("nsol"), I(1)),
                LET("header", STRCAT(S("Solution #"), STRCAT(TOSTR(V("nsol1")), S(":"))),
                LET("_p1", PRINT(V("header")),
                LET("_p2", APP2(V("print_board_f"), V("bd"), I(0)),
                LET("_p3", PRINT(S("")),
                    V("nsol1")
                ))))),
                # try_col(bd, row, 0, nsol)
                APP(V("solver"), TUP(I(1), TUP(V("bd"), TUP(V("row"), TUP(I(0), V("nsol"))))))
            ),
            # TRY_COL mode
            IF0(GTE(V("col"), I(8)),
                V("nsol"),
                LET("safe", APP4(V("safety_test2_f"), V("bd"), V("row"), V("col"), V("row")),
                    IF0(V("safe"),
                        LET("bd2", APP3(V("board_set_f"), V("bd"), V("row"), V("col")),
                        LET("nsol2", APP(V("solver"),
                                         TUP(I(0), TUP(V("bd2"), TUP(ADD(V("row"), I(1)), TUP(I(0), V("nsol")))))),
                            APP(V("solver"),
                                TUP(I(1), TUP(V("bd"), TUP(V("row"), TUP(ADD(V("col"), I(1)), V("nsol2"))))))
                        )),
                        APP(V("solver"),
                            TUP(I(1), TUP(V("bd"), TUP(V("row"), TUP(ADD(V("col"), I(1)), V("nsol"))))))
                    )
                )
            )
        )
    )))))
)

############################################################
# Main program
############################################################

queens_program = \
    LET("my_abs", my_abs,
    LET("board_get_f", board_get,
    LET("board_set_f", board_set,
    LET("safety_test1_f", safety_test1,
    LET("safety_test2_f", safety_test2,
    LET("build_row_f", build_row,
    LET("print_board_f", print_board_fn,
    LET("solver_f", solver,
    LET("empty", empty_board,
        APP(V("solver_f"), TUP(I(0), TUP(V("empty"), TUP(I(0), TUP(I(0), I(0))))))
    )))))))))

############################################################
# Transpile to JS
############################################################
print("Transpiling 8-queens to JS...")
js_code = dexp_trx2js(queens_program)

full_js = "var result = " + js_code + ';\nconsole.log("Total solutions: " + result);\n'

with open("./queens.js", "w") as f:
    f.write(full_js)

print("Written to queens.js (" + str(len(js_code)) + " chars)")

# TEST Directory — LAMBDA Compiler Tests

## Overview

Each test file constructs LAMBDA programs as `dexp` ASTs in Python,
runs type inference (`dexp_tinfer`), transpiles to JavaScript (`dexp_trx2js`),
and writes the JS output to a `.js` file that can be executed with Node.js.

## Running Tests

From the project root directory:

    bash TEST/run_all.sh

This runs each Python test (type-check + JS generation) and then
executes the generated JS in Node.js.

## Test Files

| File               | What it tests                                      | Expected JS output         |
|--------------------|----------------------------------------------------|-----------------------------|
| test_basics.py     | Int, bool, string literals; arithmetic; comparison | 42, true, "hello", 3, true |
| test_lambda.py     | Typed/untyped lambda, application, let, if-else    | 10, 1, 43                  |
| test_tuples.py     | Tuple construction, fst, snd, nested tuples        | [1,true], 1, true, 3       |
| test_recursion.py  | DEfix/DEfix1 factorial (recursive + tail-recursive)| 3628800 (three times)      |
| test_lists.py      | List nil/cons, head/tail/length, recursive sum     | [1,2,3], 1, [2,3], 3, 6   |
| test_advanced.py   | Arrays, lazy, streams, annotations, Church nums, map | Various (see file)       |
| test_queens.py     | 8-Queens puzzle (backtracking solver)               | 92 solutions printed       |

## Known Issues

- No parser: programs are constructed as Python AST objects, not parsed from
  source text. This is by design — the assignment specifies the language via
  the `dexp`/`styp` datatypes.
- The `cmp` operator emits its arguments twice in the JS ternary expression.
  If the arguments have side effects, they would be evaluated multiple times.
  In practice this does not affect any of the test programs.
- Closure conversion is not implemented. The generated JS contains nested
  function expressions (inner functions).

## Status

All 7 tests pass: type inference succeeds and the generated JavaScript
executes correctly in Node.js, producing expected output.

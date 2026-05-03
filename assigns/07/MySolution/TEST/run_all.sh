#!/bin/bash
# Run all LAMBDA test programs
# Each test: (1) runs Python to type-check and generate JS, (2) runs the JS in Node

set -e
cd "$(dirname "$0")/.."
export PYTHONPATH="$(pwd):$PYTHONPATH"

echo "============================================================"
echo "Running all LAMBDA compiler tests"
echo "============================================================"
echo ""

PASS=0
FAIL=0

for test in TEST/test_basics TEST/test_lambda TEST/test_tuples TEST/test_recursion TEST/test_lists TEST/test_advanced TEST/test_queens; do
    name=$(basename "$test")
    echo "------------------------------------------------------------"
    echo "[$name] Running Python (type-check + JS generation)..."
    echo "------------------------------------------------------------"
    if python3 "${test}.py"; then
        echo ""
        echo "[$name] Running generated JS in Node..."
        jsfile="${test}.js"
        if [ -f "$jsfile" ]; then
            if node "$jsfile" > "${test}.out" 2>&1; then
                echo "[$name] JS executed successfully."
                # Show first few lines of output
                head -5 "${test}.out"
                lines=$(wc -l < "${test}.out")
                if [ "$lines" -gt 5 ]; then
                    echo "  ... ($lines lines total)"
                fi
                PASS=$((PASS + 1))
            else
                echo "[$name] JS execution FAILED:"
                cat "${test}.out"
                FAIL=$((FAIL + 1))
            fi
        else
            echo "[$name] No JS file generated."
            FAIL=$((FAIL + 1))
        fi
    else
        echo "[$name] Python FAILED"
        FAIL=$((FAIL + 1))
    fi
    echo ""
done

echo "============================================================"
echo "Results: $PASS passed, $FAIL failed"
echo "============================================================"

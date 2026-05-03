#!/bin/bash
# Remove generated .js and .out files from TEST directory
cd "$(dirname "$0")"
rm -f *.js *.out
echo "Cleaned TEST directory."

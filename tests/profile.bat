python -m cProfile -o program.prof test_unittest.py
start /b python gprof2dot.py -f prof program.prof | dot -Tpng -o output.png
snakeviz program.prof

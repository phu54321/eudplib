python -m cProfile -o output.pstats test1.py
gprof2dot.py -f pstats output.pstats | dot -Tpng -o output.png
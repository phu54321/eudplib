python -m cProfile -o output.pstats testcreep.py
python gprof2dot.py -f pstats output.pstats | dot -Tpng -o output.png
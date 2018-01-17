@echo off
kernprof -l test_unittest.py
python -m line_profiler .\test_unittest.py.lprof
pause

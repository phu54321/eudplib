import os
import subprocess
import datetime
import time


curTime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

print("Running script")
st = time.time()
os.system("kernprof -l test_unittest.py")
print("Execute time = %fs" % (time.time() - st))

profile_result = subprocess.check_output(
    "python -m line_profiler test_unittest.py.lprof",
    shell=True
).decode('utf-8').replace("\r\n", "\n")
print(profile_result)

with open('lprof_log.txt', 'a') as lprof_fp:
    lprof_fp.write("[%s]\n%s\n\n\n" % (curTime, profile_result))

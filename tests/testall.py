import os

pytests = os.listdir()
pytests = filter(lambda x: os.path.isfile(x), pytests)
pytests = filter(lambda x: x[:4] == 'test' and x[-3:] == '.py', pytests)
pytests = list(pytests)
pytests.remove('testall.py')

for pytest in pytests:
    print('===== Testing file %s' % pytest)
    os.system("python3 \"%s\"" % pytest)
    print('---------------------------------\n')

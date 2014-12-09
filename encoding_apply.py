import os

encoding_str = '''\
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

print('Auto "# -*- coding: utf-8 -*-" inserter')

for root, dirs, files in os.walk('eudtrg'):
    for f in files:
        if f[-3:] == '.py':
            finalpath = os.path.join(root, f)
            code = open(finalpath, 'r', encoding='utf-8').read()
            if not code.startswith(encoding_str):
                print('%s' % finalpath)
                code = encoding_str + code
                open(finalpath, 'w', encoding='utf-8').write(code)

print('end')

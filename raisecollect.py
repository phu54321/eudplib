'''
Collect all assertion statements & raises. Refer when creating documentation.
'''

import os

root = 'eudtrg/'

for dirname, _, filelist in os.walk(root):
    for fname in filelist:
        if fname[-3:] == '.py':
            absp = os.path.join(dirname, fname)
            fcontent = open(absp, 'r', encoding = 'utf-8').read()
            fcontent = fcontent.split('\n')

            for lineno, fline in enumerate(fcontent):
                fline = fline.strip()

                if fline[:6] == 'raise ' or fline[:7] == 'assert ':
                    print('[%s/%s Line %d] %s' % (dirname, fname, lineno, fline))
                    #print('\n'.join(fcontent[lineno - 3 : lineno + 3]))
                    #print('\n============================================================\n')
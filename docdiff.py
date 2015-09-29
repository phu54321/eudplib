import eudplib
import types
import re

module_to_doc = eudplib

exclude_types = [dict, str, types.ModuleType]
eudftypes = [eudplib.core.varfunc.eudf.EUDFuncN]
allowed_type = eudftypes + [type, types.FunctionType]
exclude_names = ['__loader__', '__path__', '__spec__']
section_header_charr = ['=', '-', '\'', '~', '^']


# Get list of already documented items
print('Getting list of currently documented structures')
rstinputs = open('api.rst', 'r', encoding='utf-8').read().split('\n')
documented_functions = set()
documented_classes = set()

func_regex = re.compile(r'\.\. autofunction:: +eudplib\.(.+)')
class_regex = re.compile(r'\.\. autoclass:: +eudplib\.(.+)')

for line in rstinputs:
    func_match_result = func_regex.match(line)
    if func_match_result:
        funcname = func_match_result.groups(1)[0]
        if funcname in documented_functions:
            print('[Warning] Document duplication of function %s.' % funcname)
        documented_functions.add(funcname)
        continue

    class_match_result = class_regex.match(line)
    if class_match_result:
        classname = class_match_result.groups(1)[0]
        if classname in documented_classes:
            print('[Warning] Document duplication of class %s.' % classname)
        documented_classes.add(classname)
        continue


print('Collecting list of documentation-needed structures')
doc_needed_functions = set()
doc_needed_classes = set()
fc_documented = {}


# Document module
for name, value in module_to_doc.__dict__.items():
    # Exclude list
    if name in exclude_names or type(value) in exclude_types:
        continue

    # Undocumented -> ignore
    if type(value) not in allowed_type:
        continue

    if value.__doc__ is None:
        documented = False

    else:
        documented = True

    if isinstance(value, types.FunctionType) or type(value) in eudftypes:
        doc_needed_functions.add(name)
        fc_documented[name] = documented

    elif type(value) is type:
        doc_needed_classes.add(name)
        fc_documented[name] = documented

print('\n==================================\n')


# Summary
'''
print('Current entries:')
print('  Functions:')
for k in doc_needed_functions:
    print('    - %s' % k)
print('  Classes:')
for k in doc_needed_classes:
    print('    - %s' % k)
print('==================================')
'''

# Diff
unused_functions = documented_functions.difference(doc_needed_functions)
unused_classes = documented_classes.difference(doc_needed_classes)

if unused_functions or unused_classes:
    print('Entrys now unused:')
    if unused_functions:
        print('  Unused functions:')
        for k in sorted(list(unused_functions)):
            print('    - %s' % k)

    if unused_classes:
        print('  Unused classes:')
        for k in sorted(list(unused_classes)):
            print('    - %s' % k)

    print('\n==================================\n')


# Diff2
used_functions = doc_needed_functions.difference(documented_functions)
used_classes = doc_needed_classes.difference(documented_classes)

if used_functions or used_classes:
    print('New entries:')
    if used_functions:
        print('  New functions:')
        for k in sorted(list(used_functions)):
            print('    - %s %s' %
                  (k, "(Undocumented)" if not fc_documented[k] else ""))

    if used_classes:
        print('  New classes:')
        for k in sorted(list(used_classes)):
            print('    - %s %s' %
                  (k, "(Undocumented)" if not fc_documented[k] else ""))

    print('\n==================================\n')

print('Diff done')

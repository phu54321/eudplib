import eudtrglib
import types
import textwrap
import re

module_to_doc = eudtrglib

exclude_types = [dict, str, types.ModuleType]
exclude_names = ['__loader__', '__path__', '__spec__']
section_header_charr = ['=', '-', '\'', '~', '^']


# Get list of already documented items
print('Getting list of currently documented structures')
rstinputs = open('docs/api.rst', 'r', encoding = 'utf-8').read().split('\n')
documented_functions = set()
documented_classes = set()

func_regex  = re.compile(r'\.\. autofunction:: +eudtrglib\.(.+)')
class_regex = re.compile(r'\.\. autoclass:: +eudtrglib\.(.+)')

for line in rstinputs:
    func_match_result = func_regex.match(line)
    if func_match_result:
        funcname = func_match_result.groups(1)[0]
        if funcname in documented_functions:
            print('[Warning] Duplicated function name %s was documented.' % funcname)
        documented_functions.add(funcname)
        continue

    class_match_result = class_regex.match(line)
    if class_match_result:
        classname = class_match_result.groups(1)[0]
        if classname in documented_classes:
            print('[Warning] Duplicated class name %s was documented.' % classname)
        documented_classes.add(classname)
        continue


print('Collecting list of documentation-needed structures')
doc_needed_functions = set()
doc_needed_classes = set()


# Document module
for name, value in module_to_doc.__dict__.items():
    # Exclude list
    if name in exclude_names or type(value) in exclude_types:
        continue

    # Undocumented -> ignore
    if value.__doc__ is None:
        continue

    if type(value) is types.FunctionType:
        doc_needed_functions.add(name)

    elif type(value) is type:
        doc_needed_classes.add(name)

print('==================================')


# Summary
print('Current entries:')

print('  Functions:')
for k in doc_needed_functions:
    print('    - %s' % k)

print('  Classes:')
for k in doc_needed_classes:
    print('    - %s' % k)

print('==================================')

# Diff
unused_functions = documented_functions.difference(doc_needed_functions)
unused_classes = documented_classes.difference(doc_needed_classes)

if unused_functions or unused_classes:
    print('Entrys now unused:')
    if unused_functions:
        print('  Unused functions:')
        for k in unused_functions:
            print('    - %s' % k)

    if unused_classes:
        print('  Unused classes:')
        for k in unused_classes:
            print('    - %s' % k)

    print('==================================')


# Diff2
used_functions = doc_needed_functions.difference(documented_functions)
used_classes = doc_needed_classes.difference(documented_classes)

if used_functions or used_classes:
    print('New entries:')
    if used_functions:
        print('  New functions:')
        for k in used_functions:
            print('    - %s' % k)

    if used_classes:
        print('  New classes:')
        for k in used_classes:
            print('    - %s' % k)

    print('==================================')

print('Diff done')

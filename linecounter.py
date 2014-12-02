import os

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

totlinen = 0
totstrlist = []

lexer = get_lexer_by_name("python", stripall=True)
formatter = HtmlFormatter(linenos=True)

for root, dirs, files in os.walk('eudtrg'):
    for f in files:
        if f[-3:] == '.py':
            finalpath = os.path.join(root, f)
            code = open(finalpath, 'r').read()
            linen = code.count('\n') + 1
            print("%-40s : %4d" % (finalpath, linen))
            totlinen += linen

            highlighted_code = highlight(code, lexer, formatter)

            totstrlist.append(
                '<p><h2> {finalpath} : {linen} lines </h2></p>\n'
                '{highlighted_code}<br><br>'.format(**locals()))

print('Total lines: %d' % totlinen)

cssstyle = HtmlFormatter().get_style_defs('.highlight')

totstr = ''.join(totstrlist)

open('out.html', 'w').write('''\
<html>
<head>
<title> Output </title>
<style>{cssstyle}</style>
</head>
<body>
{totstr}
</body>
</html>
'''.format(**locals()))

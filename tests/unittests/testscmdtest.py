from eudplib import *


def test_static_scmdstr():
    assert SCMD2Text("<04>Test<06>") == '\x04Test\x06'
    assert SCMD2Text("<<04>Test<06>") == '<\x04Test\x06'
    assert SCMD2Text("<04><T>est<06>") == '\x04<T>est\x06'
    assert SCMD2Text("<04>Test<06>") == '\x04Test\x06'
    assert SCMD2Text("<04>Test<06>") == '\x04Test\x06'

test_static_scmdstr()

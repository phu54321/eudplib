'''
Unicode(python) <-> Binary(starcraft) conversion. Used internally in eudtrg.
'''

 

charset = 'cp949'  # default : korean


def UbconvUseCharset(newencoding):
    global charset
    charset = newencoding


def Unicode2Bytes(string):
    if isinstance(string, bytes):
        return string

    elif isinstance(string, str):
        return string.encode(charset)

    else:
        raise TypeError(
            'Unknown type %s given to Unicode2Bytes' % type(string))


def Bytes2Unicode(b):
    if isinstance(b, str):
        return b

    elif isinstance(b, bytes):
        return b.decode(charset)

    else:
        raise TypeError('Unknown type %s given to Bytes2Unicode' % type(b))


def main():
    print("Performing unicode - multibyte conversion library")

if __name__ == "__main__":
    main()

# shorter names
u2b = Unicode2Bytes
b2u = Bytes2Unicode

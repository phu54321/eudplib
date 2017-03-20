import sys
import eudplib as ep

traceDB = ep.Db(b'profiled_magicid\0\0\0\0')
traceMemory = traceDB + 16
traceFileMap = {}


def addTraceMarker(fname, line):
    try:
        traceFileID, traceFileLines = traceFileMap[fname]
    except KeyError:
        traceFileID = len(traceFileMap)
        traceFileMap[fname] = traceFileID

    dw = (traceFileID << 16) | line
    ep.DoActions(ep.SetMemory(traceMemory, ep.SetTo, dw))


def resetTraceMarker():
    ep.DoActions(ep.SetMemory(traceMemory, ep.SetTo, 0))


def traceFunction(frame, event, arg):
    cff = ep.GetCurrentCompiledFunc()
    if event == 'call':
        co = frame.f_code
        if cff and co == cff._bodyfunc.__code__:
            return traceFunction
        else:
            return None

    else:
        # Add only if function line is within current function code
        co = frame.f_code
        if co == cff._bodyfunc.__code__:
            if event == 'line':
                addTraceMarker(co.co_filename, frame.f_lineno)
            else:
                resetTraceMarker()


oldTraceFunc = None


def applyProfiling():
    global oldTraceFunc
    oldTraceFunc = sys.gettrace()
    sys.settrace(traceFunction)


def dumpProfileMap():
    global oldTraceFunc

    sys.settrace(oldTraceFunc)
    oldTraceFunc = None
    sbuf = []
    for fname, fid in traceFileMap:
        sbuf.append("%s\t%d\n" % (fname, fid))

    return ''.join(sbuf)


applyProfiling()

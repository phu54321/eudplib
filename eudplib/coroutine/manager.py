from .. import (
    core as c,
    ctrlstru as cs,
    eudlib as sf,
)


class CoroutineData(c.Expr):
    def __init__(self):
        self._data = sf.EUDArray(3)

    def Evaluate(self):
        return c.Evaluate(self._data)

    def getPrev(self):
        return self._data[0]

    def getNext(self):
        return self._data[1]

    def getJumper(self):
        return self._data[2]

    def setPrev(self, data):
        self._data[0] = data

    def setNext(self, data):
        self._data[1] = data

    def setJumper(self, data):
        self._data[2] = data


class CoroutineManager:
    def __init__(self):
        self._head = CoroutineData()
        self._head.setPrev(self._head)
        self._head.setNext(self._next)
        self._head.setJumper(0x00000000)

        self._currentNode = c.EUDVariable(self._head)

    # --------

    def destroyNode(self, node):
        prevNode = self._head.getPrev()
        nextNode = self._head.getNext()

        cs.DoActions([
            c.SetMemory(prevNode + 4, c.SetTo, nextNode),
            c.SetMemory(nextNode, c.SetTo, prevNode)
        ])

        return nextNode

    def addNode(self, prevNode, node):
        nextNode = prevNode.getNext()

        cs.DoActions([
            c.SetMemory(node, c.SetTo, prevNode),
            c.SetMemory(prevNode + 4, c.SetTo, node),
            c.SetMemory(node + 4, c.SetTo, nextNode),
            c.SetMemory(nextNode, c.SetTo, node)
        ])

    # --------

    def gotoNextNode(self):
        resumePoint = c.Forward()

        currentNode = self._currentNode
        currentNode.setJumper(resumePoint)
        nextNode = currentNode.getNext()
        self._currentNode << nextNode
        t = c.Forward()
        cs.DoActions(c.SetNextPtr(t, nextNode))
        t << c.RawTrigger()

        resumePoint << c.NextTrigger()
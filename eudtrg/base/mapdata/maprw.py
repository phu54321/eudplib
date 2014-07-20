'''
Implements LoadMap, SaveMap function
'''

from eudtrg import LICENSE #@UnusedImport

from ..dataspec.trigger import Trigger

from .mapdata import (
    locnametable,
    unitnametable,
    strtable,
    uprptable,
    uprpdict
)

from ..utils import binio
from . import chktok, mpqapi
from ..inject import injgen
from .nametable import ParseString

# private variables
_chk = None
_mpqcontent = None



def PutDict_NoDup(d, key, value):
    if key in d: # Duplication
        d[key] = None # Mark as duplicate
    else:
        d[key] = value

    


def LoadMap(fname):
    '''
    Load template map and read various data from it.

    :param fname: Path to input map.
    '''

    print('Loading map %s' % fname)


    global _chk, _mpqcontent
    
    # read mpq content. The file will be copied to output file.
    _mpqcontent = open(fname, 'rb').read()
    
    
    # open mpq file
    mr = mpqapi.MpqRead()
    if not mr.Open(fname):
        raise RuntimeError('Failed to open map file \'%s\'.' % fname)
    
    # extract scenario.chk
    rawchk = mr.Extract('staredit\\scenario.chk')
    chk = chktok.CHK()
    chk.loadchk(rawchk)
    _chk = chk
    
    # Delete unwanted sections.
    chk.delsection('SWNM') # Switch names are ignored in eudtrg.
    chk.delsection('UPRP') # Unit properties are ignored here.
    chk.delsection('UPUS') # related to uprp
            
    
    # Load STR section    
    strtable.LoadTBL(_chk.getsection('STR'))
    
    
    # Init nametables
    locnametable.clear()
    unitnametable.clear()

    # Function for ignoring unit name color.
    def IgnoreColor(s):
        stb = []
        for ch in s:
            if 0x01 <= ch <= 0x1F or ch == 0x7F: # Special characters.
                continue
            else:
                stb.append(bytes([ch]))

        return b''.join(stb)



    # Get location names
    mrgn = _chk.getsection('MRGN')
    if mrgn:
        locn = len(mrgn) // 20
        for i in range(locn):
            locstrid = binio.b2i2(mrgn, i*20 + 16)
            locstr = strtable.GetString(locstrid)
            if not locstr: continue

            PutDict_NoDup(locnametable, locstr, i+1) # SC counts location from 1. Weird


    # Get unit names
    unix = _chk.getsection('UNIx')
    if unix:
        for i in range(228):
            unitstrid = binio.b2i2(unix, 3192 + i * 2)
            unitstr = strtable.GetString(unitstrid)
            if not unitstr: continue


            PutDict_NoDup(unitnametable, unitstr, i)
            cignored = IgnoreColor(unitstr)
            if cignored != unitstr:
                PutDict_NoDup(unitnametable, cignored, i)
                
    
    uprptable.clear()
    uprpdict.clear()
    
    
    


def SaveMap(fname, root, additionalfiles = {}):
    '''
    Save template map with EUDObjects & various files.

    :param root: Starting trigger. At every trigger loop, a computer player
        executes triggers starting from root.
    
    :param additionalfiles: List of (MPQ Filename, bytes) to be inserted into
        map MPQ. If different contents share the same MPQ filename, function
        will raise RuntimeError.
    '''

    print('Saving map %s' % fname)

    # Message to display for non EUDA-Enabled players
    # Since we pass in strtable.SaveTBL() into injgen.GenerateInjector, injgen
    # cannot insert new string into string table. So we first make one and pass
    # it to injgen
    eudenabler_needed = ParseString('This map requires EUD Action Enabler to run.')
    

    # write new uprp
    uprpcontent = b''.join( uprptable + [bytes(20 * (64 - len(uprptable)))] )
    _chk.setsection('UPRP', uprpcontent)
    
    # write new str
    strcontent = strtable.SaveTBL()
    _chk.setsection('STR', strcontent)
    
    # Generate injector
    injgen.GenerateInjector(_chk, root, eudenabler_needed)
    
    # optimize & dump
    _chk.optimize()
    rawchk = _chk.savechk()
    
    # dump mpq content and modify it
    open(fname, 'wb').write(_mpqcontent)
    mw = mpqapi.MpqWrite()
    if not mw.Open(fname, preserve_content = True):
        raise RuntimeError('Cannot open output file \'%s\'.' % _mpqcontent)


    mw.PutFile('staredit\\scenario.chk', rawchk)


    # Put in additional files
    for fname, data in additionalfiles.items():
        mw.PutFile(fname, data)

    # Compact & close
    mw.Compact()
    mw.Close()

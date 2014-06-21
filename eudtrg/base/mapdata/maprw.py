'''
Implements LoadMap, SaveMap function
'''

from eudtrg import LICENSE #@UnusedImport

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

# private variables
_chk = None
_mpqcontent = None

    
def LoadMap(fname):
    '''
    Load template map and read various data from it.
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

    # Get location names
    mrgn = _chk.getsection('MRGN')
    if mrgn:
        locn = len(mrgn) // 20
        for i in range(locn):
            locstrid = binio.b2i2(mrgn, i*20 + 16)
            locstr = strtable.GetString(locstrid)
            if not locstr: continue

            if locstr in locnametable: # Location name duplicated
                locnametable[locstr] = None
            else:
                locnametable[locstr] = i + 1 # SC counts location from 1. Weird

    # Get unit names
    unix = _chk.getsection('UNIx')
    if unix:
        for i in range(228):
            unitstrid = binio.b2i2(unix, 3192 + i * 2)
            unitstr = strtable.GetString(unitstrid)
            if not unitstr: continue

            if unitstr in unitnametable:
                unitnametable[unitstr] = None # Unit name duplicated
            else:
                unitnametable[unitstr] = i
                
    
    uprptable.clear()
    uprpdict.clear()
    # No entry is needed now.
    
    
    
def SaveMap(fname, root):
    '''
    Inject EUDObjects needed for roots into template map and save it to fname.
    Original map file is not altered.
    '''

    print('Saving map %s' % fname)
   
    # write new uprp
    uprpcontent = b''.join( uprptable + [bytes(20 * (64 - len(uprptable)))] )
    _chk.setsection('UPRP', uprpcontent)
    
    # write new str
    strcontent = strtable.SaveTBL()
    _chk.setsection('STR', strcontent)
    
    # Generate injector
    injgen.GenerateInjector(_chk, root)
    
    # optimize & dump
    _chk.optimize()
    rawchk = _chk.savechk()
    
    # dump mpq content and modify it
    open(fname, 'wb').write(_mpqcontent)
    mw = mpqapi.MpqWrite()
    if not mw.Open(fname, preserve_content = True):
        raise RuntimeError('Cannot open output file \'%s\'.' % _mpqcontent)


    mw.PutFile('staredit\\scenario.chk', rawchk)
    mw.Compact()
    mw.Close()

from eudtrg import LICENSE

from ..utils.binio import *
from ..utils.sctbl import TBL
from .trigtrg import *

"""
One button trigger injector.
 - root            : First trigger to be executed.
"""

def GenerateInjector(chkt, roots):
    # Get needed sections
    section_str = chkt.getsection('STR')
    section_mrgn = chkt.getsection('MRGN')

    # Insert notification string
    # This is kinda weird, since we're unpacking STR table that were just been packed at SaveMap
    # I couldn't find a better way to get string number of 'This map requires EUD Action Enabler to run.'
    # while not creating the same string inside SaveMap. This works, so it's done.
    stb = TBL(section_str)
    noneuda_notify = stb.GetStringIndex('This map requires EUD Action Enabler to run.')
    section_str = stb.SaveTBL()

    '''
    What we'll do:

    struct PlayerTriggerStruct {
        DWORD unk, prev, next;
    };


    DWORD old_pts_first[8]; // Vanilla Location Table
    DWORD old_pts_last[8]; // Vanilla Location Table
    const int payload_offset; // pregiven

    const BYTE* mrgn = (BYTE*)0x58DC60;
    const PlayerTriggerStruct *pts  = (PlayerTriggerStruct*)0x51A280;

    // 1. backup old pts data
    for(int i = 0 ; i < 8 ; i++) {
        old_pts_last[i] = pts[i].prev;
        old_pts_first[i] = pts[i].next;
    }

    // 2. MRGN-TRIG link
    for(int i = 0 ; i < 8 ; i++) {
        if(currentplayer == i) {
            *(DWORD*)(mrgn + 4) = old_pts_last[i];
            *(DWORD*)(pts[i].next + 4) = mrgn; // uses current player trick
        }
    }
    *(DWORD*)(mrgn + 8 + 320 + 2048) = 4; // Preserve Trigger

    
    // 3. Init PRT Applier
    for(int i = 0 ; i < 32 ; i++) {
        *(DWORD*)(mrgn + 8 + 320 + 32*i + 16) = EPD(str + payload_offset);
        *(DWORD*)(mrgn + 8 + 320 + 32*i + 20) = (str + payload_offset) // 4;
        *(DWORD*)(mrgn + 8 + 320 + 32*i + 24) = 0x082D0000;
    }

    // 4. Run PRT Applier



    *(DWORD*)(0x51A280 + 8 + 12*i) = 58CD60 //

    if(player == i) *(DWORD*)(

    '''
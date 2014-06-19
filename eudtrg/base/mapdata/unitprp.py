from eudtrg import LICENSE #@UnusedImport

from ctypes import * #@UnusedWildImport

class UnitProperty(LittleEndianStructure):
    _fields_ = [
        ('sprpvalid', c_ushort),
        ('prpvalid', c_ushort),
        ('player', c_byte),
        ('hitpoint', c_byte),
        ('shield', c_byte),
        ('energy', c_byte),
        ('resource', c_uint),
        ('hanger', c_ushort),
        ('sprpflag', c_ushort),
        ('unused', c_uint)
    ]
        
    def __init__(self,
        # Properties. True/False/None(Don't care)
        hitpoint = None, shield = None, energy = None, resource = None, hanger = None,
        # Special properties. True/False/None(Don't care)
        clocked = None, burrowed = None, intransit = None, hallucinated = None, invincible = None
    ):
        assert hitpoint is None or 0 <= hitpoint <= 100
        assert shield is None or 0 <= shield <= 100
        assert energy is None or 0 <= energy <= 100
        assert resource is None or 0 <= resource
        assert hanger is None or 0 <= hanger <= 255
        
        assert clocked in [None, True, False]
        assert burrowed in [None, True, False]
        assert intransit in [None, True, False]
        assert hallucinated in [None, True, False]
        assert invincible in [None, True, False]
        
        def prop2int(p):
            if p is None: return 0
            else: return p
            
        def prop2valid(p, v):
            if p is None: return 0
            else: return v
        
        def prop2flag(p, v):
            if p: return v
            else: return 0
        
        self.player = 0
        
        # Set properties
        self.hitpoint = prop2int(hitpoint)
        self.shield = prop2int(shield)
        self.energy = prop2int(energy)
        self.resource = prop2int(resource)
        self.hanger = prop2int(hanger)
        
        self.prpvalid = (
            prop2valid(hitpoint, 1<<1) |
            prop2valid(shield,   1<<2) |
            prop2valid(energy,   1<<3) |
            prop2valid(resource, 1<<4) |
            prop2valid(hanger,   1<<5)
        )
        
        # Set special properties
        self.sprpvalid = (
            prop2valid(clocked,      1<<0) |
            prop2valid(burrowed,     1<<1) |
            prop2valid(intransit,    1<<2) |
            prop2valid(hallucinated, 1<<3) |
            prop2valid(invincible,   1<<4)
        )
        
        self.sprpflag = (
            prop2flag(clocked,      1<<0) |
            prop2flag(burrowed,     1<<1) |
            prop2flag(intransit,    1<<2) |
            prop2flag(hallucinated, 1<<3) |
            prop2flag(invincible,   1<<4)
        )
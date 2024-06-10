# eudplib

Implementation of EUD-based structural programming on [Starcraft](https://us.shop.battle.net/ko-kr/family/starcraft-remastered). Starcraft only supports basic conditional `if(~) { actions; }` blocks called 'Triggers'. No `else`, no variables, no `while` or `for` loops, no functions, and no pointers. Nothing. eudplib framework hijacks Starcraft's trigger system to implement all these structural programming schemes.

eudplib allows basic C-level programming on Starcraft. See [binary searching with function pointer](https://github.com/phu54321/eudplib/blob/master/tests/unittests/testbinsearch.py) as an example. This code showcases function, function pointer, and variable usage.

```py
from helper import *

@TestInstance
def test_binsearch():
    n = EUDVariable()

    # Basic test
    n << 1000
    p1 = EUDBinaryMin(lambda x: x * x >= n, 0, 0xffff)
    p2 = EUDBinaryMax(lambda x: x * x <= n, 0, 0xffff)
    test_equality(
        "Binary search - Square root test",
        [p1, p2], [32, 31]
    )

    # Specific range test
    @EUDFunc
    def comp1(x):
        if EUDIf()(x <= 30):
            EUDReturn(0)
        if EUDElseIf()(x >= 70):
            EUDReturn(0)
        if EUDElseIf()(x <= 40):
            EUDReturn(1)
        if EUDElse()():
            EUDReturn(0)
        EUDEndIf()
    p3 = EUDBinaryMax(comp1, 31, 69)

    @EUDFunc
    def comp1(x):
        if EUDIf()(x <= 30):
            EUDReturn(0)
        if EUDElseIf()(x >= 70):
            EUDReturn(0)
        if EUDElseIf()(x >= 40):
            EUDReturn(1)
        if EUDElse()():
            EUDReturn(0)
        EUDEndIf()
    p4 = EUDBinaryMin(comp1, 31, 69)

    test_equality(
        "Binary search - bounded range test",
        [p3, p4], [40, 40]
    )
```

eudplib also implements a simple script language called **"epScript"**. Because eudplib relies on Python for code generation, it has a lot of its hiccups, like double parenthesis  on `if EUDIf()(x <= 30):`. epScript wraps these messy things into a very ECMAscript-like language. Check out [Roulette](https://github.com/phu54321/Roulette) for such implementations.

```js
function rouletteLoop() {
    var prevAngle = theta / angle_multiplier;
    roulettePhysics();
    var newAngle = theta / angle_multiplier;

    prevAngle += (newAngle - prevAngle + cossin.angleNum) % cossin.subSubAngleNum;

    while(1) {
        const c, s = cossin.roulette_lengthdir(r, prevAngle);
        const x, y = -s, -c;
        const cx, cy = 128 * 32, 128 * 32;
        loc.pxMoveTo(x + cx, y + cy);

        if (prevAngle == newAngle) {
            utils.createPassableUnit("Ball", "pxMove", P7);
            KillUnit("Ball", Force2);
            break;
        }
        else {
            utils.createPassableUnit("Ball", "pxMove", P8);
        }

        prevAngle = (prevAngle + cossin.subSubAngleNum) % (cossin.angleNum);
    }
 }
 ```

 You can learn more about programming in eudplib & epscript on [EDAC](https://cafe.naver.com/edac) cafe.

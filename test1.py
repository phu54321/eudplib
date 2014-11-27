import eudtrg as et

a = et.Trigger(
    conditions=[
        et.Memory(0x58A364, et.AtLeast, 30)
    ],
    actions=[
        et.SetMemory(0x58A364, et.Add, 30)
    ]
)

b = et.Trigger(
    conditions=[
        et.Memory(0x58A364, et.AtLeast, 30)
    ],
    actions=[
        et.SetMemory(0x58A364, et.Add, 30)
    ]
)

et.Trigger(nextptr=0x80000000)

pl = et.allocator.payload.CreatePayload(a)

open('out.bin', 'wb').write(pl.data)
print(pl.prttable)
print(pl.orttable)

cdef unsigned int cryptTable[0x500]

cdef _InitCryptTable():
    cdef unsigned int seed = 0x00100001
    cdef unsigned int index1 = 0, index2 = 0, i
    cdef unsigned int temp1, temp2

    for index1 in range(0x100):
        index2 = index1
        for _ in range(5):
            seed = (seed * 125 + 3) % 0x2AAAAB
            temp1 = (seed & 0xFFFF) << 0x10

            seed = (seed * 125 + 3) % 0x2AAAAB
            temp2 = seed % 0xFFFF

            cryptTable[index2] = temp1 | temp2
            index2 += 0x100

_InitCryptTable()

# -----

def DecryptDwords(unsigned int blocks[]):
    cdef unsigned int seed = 0xFFFFFFFF

    for dw in dword:
        seed += cryptTable[0x400 + (key & 0xFF)]
        ch = dw ^ (key + seed)

        key = ((~key << 0x15) + 0x11111111) | (key >> 0x0B)
        seed = ch + seed + (seed << 5) + 3;





void DecryptBlock(void *block, long length, unsigned long key)
{
unsigned long seed = 0xEEEEEEEE, unsigned long ch;
unsigned long *castBlock = (unsigned long *)block;

// Round to longs
length >>= 2;

while(length-- > 0)
{
seed += stormBuffer[0x400 + (key & 0xFF)];
ch = *castBlock ^ (key + seed);

key = ((~key << 0x15) + 0x11111111) | (key >> 0x0B);
seed = ch + seed + (seed << 5) + 3;
*castBlock++ = ch;
}
}
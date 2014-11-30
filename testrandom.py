bucketn = 10

x = 1
freq = [0] * bucketn

for _ in range(10000):
    x = (x * 1664525 + 1013904223) & 0xFFFFFFFF
    freq[x % bucketn] += 1

print(freq)

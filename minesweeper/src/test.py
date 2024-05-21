count = 0
for x in range(0, 10):
    for y in range(10):
        for z in range(10):
            if x == y or y == z:
                # print(f"{x}{y}{z}")
                count += 1

print("final count:", count)


count = 0

for x in range(1, 10):
    for y in range(10):
        for z in range(10):
            if (x == y and y != z) or (y == z and x != y and x != z):
                # print(f"{x}{y}{z}")
                count += 1
print("final count for exact", count)
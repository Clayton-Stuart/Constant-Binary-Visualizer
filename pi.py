# vars
fin = 0
n = 2

fin += 3

while True:
    fin += (4 / ((n)*(n+1)*(n+2)))
    n += 2
    fin -= (4 / ((n)*(n+1)*(n+2)))
    n += 2

    print(fin)
    
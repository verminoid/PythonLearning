import sys

stairs = int(sys.argv[1])

i=stairs
while i>0:
    i -= 1
    print(" "*i + "#"*(stairs-i))
    

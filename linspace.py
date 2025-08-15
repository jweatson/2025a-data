import sys
from numpy import linspace
start=int(sys.argv[1])
fin=int(sys.argv[2])
ns=int(sys.argv[3])
ll=linspace(start,fin,ns)
for l in ll:
  print(l,end=" ")
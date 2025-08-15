import sys
from numpy import logspace
start=int(sys.argv[1])
fin=int(sys.argv[2])
ns=int(sys.argv[3])
ll=logspace(start,fin,ns)
for l in ll:
  print(l,end=" ")
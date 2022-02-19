from rainbow import *

L1=Vacuum(5)  
L2=H2O(2)

x=Continuum()
x.add([L2,L1])
print(x.layers())
print(x.evaluate_field((1,1)))

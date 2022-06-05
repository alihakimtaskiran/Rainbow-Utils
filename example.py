from rainbow import *

DBR=Stack()
DBR.add_ambient(Ambient([1,]*10, [1,]*10, 'Air'))
DBR.add_substrate(Substrate([20.25]*10, [1,]*10, 'Silicone-Wafer'))

for i in range(8):
    DBR.add_layer([ThinLayer(123e-9, [4.0779]*10, [1]*10, name=f'Si3N4 {i}'), ThinLayer(151e-9, [2.1025]*10, [1]*10, name=f'SiO2 {i}') ])
for i in range(8):
    DBR.add_layer([ThinLayer(151e-9, [2.1025]*10, [1]*10, name=f'SiO2 {8+i}'), ThinLayer(123e-9, [4.0779]*10, [1]*10, name='Si3N4 {i+8}')])
DBR.Radiation(885e-9, np.deg2rad(i))
DBR.render()

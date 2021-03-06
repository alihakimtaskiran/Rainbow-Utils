DBR=Stack()
DBR.add(Ambient(1, 1, 'Air'))
DBR.add(Substrate(20.25, 1, 'Silicone-Wafer'))

for i in range(8):
    DBR.add([ThinLayer(123e-9, 4.0779, 1, name=f'Si3N4 {i}'), ThinLayer(151e-9, 2.1025, 1, name=f'SiO2 {i}') ])

DBR.Radiation(885e-9)
DBR.render()
print(f"Reflectance:{DBR.reflectance}% Transmittance:{DBR.transmittance}%")

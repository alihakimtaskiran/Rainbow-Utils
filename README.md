# Rainbow-Utils
<img src="refraction.png" width="400">
<br>
Refraction... It is apparently the most inspiring phenomenon of the light. Rainbow appears with refraction after the rain. We can see all of the vidible spectrum. Wishing to simulate it, Rainbow-Utils was created. 
<br>
Rainbow-Utils is designed to simulate multi-layer thin film stacks with Transfer Matrix Method (TMM). Layers of thin film materials, ambient and substrate  with given ε<sub>r</sub> and µ<sub>r</sub> are simulated with Rainbow-Utils

## Docs

<pre>
|----Ambient(object)------|
|                         |---__init__(e_r=1,mu_r=1,name='')
|                         |---info
|                         |---depth
|                         |---__repr__()
|
|
|----ThinLayer(object)----|
|                         |---__init__(thickness,e_r=1,mu_r=1,name='')
|                         |---depth
|                         |---info
|                         |---__repr__()
|
|
|----Substrate(object)----|
|                         |---__init__(e_r=1,mu_r=1,name='')
|                         |---info
|                         |---depth
|                         |---__repr__()
|
|
|----Stack(object)--------|
                          |---__init__()
                          |---add_layer(arg)
                          |---stack
                          |---add_substrate(arg)
                          |---add_ambient(arg)
                          |---Radiation(wavelenght,theta=0)
                          |---reflectance
                          |---transmittance
                          |---transfer_matrix
                          |---render()
                          |---__tmgen(i)
                          |---__ddp(A,B)

</pre>



# Rainbow-Utils
<img src="refraction.png" width="400">
<br>
Refraction... It is apparently the most inspiring phenomenon of the light. Rainbow appears with refraction after the rain. We can see all of the vidible spectrum. Wishing to simulate it, Rainbow-Utils was created. 
<br>
Rainbow-Utils is designed to simulate multi-layer thin film stacks with Transfer Matrix Method (TMM). Layers of thin film materials, ambient and substrate  with given ε<sub>r</sub> and µ<sub>r</sub> are simulated with Rainbow-Utils. Moreover, it is compatible with dielectric, magnetic or meta materials.

## Tree of The Module

<pre>
|----Ambient(object)------|
|                         |---__init__(e_r=1,mu_r=1,name='')
|                         |---info
|                         |---__repr__()
|
|
|----ThinLayer(object)----|
|                         |---__init__(thickness,e_r=1,mu_r=1,name='')
|                         |---info
|                         |---__repr__()
|
|
|----Substrate(object)----|
|                         |---__init__(e_r=1,mu_r=1,name='')
|                         |---info
|                         |---__repr__()
|
|
|----Stack(object)--------|
                          |---__init__()
                          |---add(arg)
                          |---stack
                          |---Radiation(wavelenght,theta=0, polarisation_mode='TM')
                          |---render()
                          |---reflectance
                          |---transmittance
                          |---TransferMatrix()

</pre>
<hr>

## Docs


### Ambient(e_r=1,mu_r=1,name='')
  It defines properties of the ambient where the thin film and substrate is used. **e_r** is relative permittivity of the material; namely square root of non-magnetic, dielectric materials. e_r may take int, float or complex. **mu_r** is relative permeability of the material. It may take int, float or complex. Additionaly, **name** is name of the material. It takes string.

### ThinLayer(thickness,e_r=1,mu_r=1,name='')
  ThinLayer object defines each of the thin film layers. **thickness** is thickness of the material with units of <u>meters</u>. It may take a float. **e_r** is relative permittivity of the material; namely square root of non-magnetic, dielectric materials. e_r may take int, float or complex. **mu_r** is relative permeability of the material. It may take int, float or complex. Additionaly, **name** is name of the material. It takes string.

### Substrate(e_r=1,mu_r=1,name='')
  It defines properties of the substrate where the thin film is coated. **e_r** is relative permittivity of the material; namely square root of non-magnetic, dielectric materials. e_r may take int, float or complex. **mu_r** is relative permeability of the material. It may take int, float or complex. Additionaly, **name** is name of the material. It takes string.

### Stack()
It composes the materials. Thin film layers are stacked on a substrate in an ambient with *Stack()* object.

- **add(arg)** : Adds a material layer, substrate or ambient to stack object. It may take Ambient, ThinLayer, Substrate or list of these objects Due to the recursion of the functiton, it may take list of tuple of list of materials; namely [A,[B, C, [D, E], F], G, H, I] 
- **stack** : It returns list of repr of added materials.
- **Radiation(wavelenght,theta=0, polarisation_mode='TM')** : It defines wavelenght, angle and polarisation mode of the radiation. **wavelenght** is a float and units of it is <u>meters</u>. **theta** is incident angle and a float, units of it is <radians</u>. **polarisation_mode** may take whether "TM" or "TE" strings.
- **render()** : Computes reflectivity, transmittance and transfer matrix of the multilayer media. Don't execute it before calling *Radiation()*
- **reflectance** : Returns rendered reflectivity parameter. Don't execute it before calling *render()*
- **transmittance** : Returns rendered reflectivity parameter. Don't execute it before calling *render()*
- TransmferMatrix() : Returns rendered transfer matrix parameter. Don't execute it before calling *render()*

<hr>

## References
[1] Liu, Xiaoze, "Control of Exciton Photon Coupling in Nano-structures" (2014). CUNY Academic Works.
https://academicworks.cuny.edu/gc_etds/491


[2] Saleh, B. E. A., & Teich, M. C. (2019). Fundamentals of 
Photonics. Newark: John Wiley & Sons, Incorporated.



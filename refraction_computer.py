import numpy as np

Ɛ=8.8541878128e-12

class H20(object):
    def __init__(self, thickness_nm):
        
        self.n=1.333-4.078e+03*1.j
        self.thickness_nm=thickness_nm
        self.Ɛ=Ɛ*np.array(((80.4 , 0),
                           (0    , 80.4)))
        
        self.material="H2O"
        

class Vacuum(object):
    def __init__(self, thickness_nm):
        self.n=1
        self.thickness_nm=thickness_nm
        self.Ɛ=Ɛ*np.array(((1 , 0),
                           (0 , 1)))
        
        self.material=None
  
possible_materials={H2O, Vacuum}


class Continuum(object):
    def __init__(self):
        self.materials=[]
    
    def layers(self):
        return [(i.material, i.thickness_nm) for i in self.materials]
    
    def add(self,material):
        if type(material)==tuple or type(material)==list:
            for m in material:
                if not type(m) in possible_materials:
                    raise TypeError(f"{m} is not a type of defined material")
            for m in material:
                self.materials.append(m)
                
        elif type(material) in possible_materials:
            self.materials.append(material)
            
    def evaluate_field(self, incoming_E):
        
        ___=type(incoming_E)
        if ___==list or ___==tuple:
            incoming_E=np.array(incoming_E)
            if incoming_E.shape==(2,):
                pass
            else:
                raise ValueError("E-field is must be a 2D vector")
        elif ___==np.array:
            if not incoming_E.shape==(2,):
                raise ValueError("E-field is must be a 2D vector")
        else:
            raise ValueError(f"{incoming_E} is not a 2D E-field vector")
    


        E=np.array((np.linalg.norm(incoming_E),np.math.atan2(incoming_E[1],incoming_E[0])))
        for n in range(1,len(self.materials)) :
            
            E[0]*=np.math.exp(self.materials[n-1].n.imag*self.materials[n-1].thickness_nm*1e-9)
            try:
                _=np.math.asin((self.materials[n-1].n.real/self.materials[n].n.real)*np.math.sin(E[1]))
                E[1]=_
            except ValueError:
                E[1]*=-1
            
        return np.array((E[0]*np.math.cos(E[1]),E[0]*np.math.sin(E[1])))

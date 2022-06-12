import numpy as np
class Ambient(object):
    def __init__(self, e_r=1, mu_r=1, name=''):
        if not isinstance(e_r, (int, float, complex)):
            raise TypeError('e_r(relative permittivity) of the ambient must be a int, flat or complex')

        if not isinstance(mu_r, (int, float, complex)):
            raise TypeError('mu_r(relative permeability) of the ambient must be a int, flat or complex')


        if not isinstance(name, str):
            raise TypeError('name must be a string')
        
        self.__e_r=e_r
        self.__mu_r=mu_r
        self.__name=name


    @property
    def info(self):
        return self.__e_r, self.__mu_r, self.__name

    def __repr__(self):
        return f'Ambient {self.__name} Relative Permittivity:{self.__e_r} Relative Permeability:{self.__mu_r}'
    
class Substrate(object):
    def __init__(self, e_r=1, mu_r=1, name=''):
        if not isinstance(e_r, (int, float, complex)):
            raise TypeError('e_r(relative permittivity) of the substrate must be a int, flat or complex')

        if not isinstance(mu_r, (int, float, complex)):
            raise TypeError('mu_r(relative permeability) of the substrate must be a int, flat or complex')


        if not isinstance(name, str):
            raise TypeError('name must be a string')
        
        self.__e_r=e_r
        self.__mu_r=mu_r
        self.__name=name


    @property
    def info(self):
        return self.__e_r, self.__mu_r, self.__name

    def __repr__(self):
        return f'Substrate {self.__name} Relative Permittivity:{self.__e_r} Relative Permeability:{self.__mu_r}'

class ThinLayer(object):
    def __init__(self, d, e_r=1, mu_r=1, name=''):
        if not isinstance(e_r, (int, float, complex)):
            raise TypeError('e_r(relative permittivity) of the ThinLayer must be a int, flat or complex')

        if not isinstance(mu_r, (int, float, complex)):
            raise TypeError('mu_r(relative permeability) of the ThinLayer must be a int, flat or complex')


        if not isinstance(name, str):
            raise TypeError('name must be a string')
        
        self.__d=d
        self.__e_r=e_r
        self.__mu_r=mu_r
        self.__name=name
        

    @property
    def info(self):
        return self.__d, self.__e_r, self.__mu_r, self.__name

    def __repr__(self):
        return f'ThinLayer {self.__name} Thickness:{self.__d*1e9} nm Relative Permittivity:{self.__e_r} Relative Permeability:{self.__mu_r}'

class Stack(object):
    def __init__(self):

        self.__layers=[]
        self.__ambient=None
        self.__substrate=None
        self.__eta=[]
        self.__n=[]
        self.__radiation=None
        self.__tm=None


    @property
    def stack(self):
        return self.__ambient, self.__layers, self.__substrate
    def add(self, arg):
        if isinstance(arg, (list, tuple)):
            for argv in arg:
                self.add(argv)
        elif isinstance(arg, Ambient):
            self.__ambient=arg
        elif isinstance(arg, Substrate):
            self.__substrate=arg
        elif isinstance(arg, ThinLayer):
            self.__layers.append(arg)
        else:
            raise TypeError('Only an Ambient, ThinLayer or Substrate can be added')

    def Radiation(self, wavelenght, theta=0, polarisation_mode='TM'):
        if polarisation_mode=='TE':
            pm=0
        elif polarisation_mode=='TM':
            pm=1
        else:
            raise ValueError('Polarization mode must be string of "TE" or "TM"')
        
        self.__radiation = np.math.pi*2/wavelenght, np.sin(theta), pm #wavenumber, theta, polarisaton_mode
   
    def render(self):
        self.__n_layers=len(self.__layers)    
        self.__n=[np.sqrt(self.__ambient.info[0]*self.__ambient.info[1])]+[np.sqrt(self.__layers[i].info[2]*self.__layers[i].info[1]) for i in range(self.__n_layers)]+[np.sqrt(self.__substrate.info[0]*self.__ambient.info[1])]
        for i in range(self.__n_layers):
            
            n_2=self.__n[i+1]
            l=self.__layers[i].info[0]
            r_12=self.__r(i, i+1)
            r_23=self.__r(i+1, i+2)

            pa=np.exp(1j*n_2*self.__radiation[0]*l)
            na=np.conj(pa)
            M_i=np.array([[pa+r_12*r_23*na, -r_12*pa-r_23*na], [-r_12*na- r_23*pa , na+r_12*r_23*pa]])
            if i!=0:
                self.__tm=np.dot(self.__tm, M_i)
            else:
                self.__tm=M_i


    def __r(self, i ,j):
        if self.__radiation[2]==0:
            return (self.__n[i]*self.__cos_theta_(i)-self.__n[j]*self.__cos_theta_(j))/(self.__n[i]*self.__cos_theta_(i)+self.__n[j]*self.__cos_theta_(j))
        elif self.__radiation[2]==1:
            return (self.__n[i]*self.__cos_theta_(j)-self.__n[j]*self.__cos_theta_(i))/(self.__n[i]*self.__cos_theta_(j)+self.__n[j]*self.__cos_theta_(i))

    def __cos_theta_(self, i):
        return np.sqrt(1 - (self.__n[0]/self.__n[i]*self.__radiation[1])**2 )

    @property
    def reflectance(self):
        return abs(self.__tm[1,0]/self.__tm[0,0])**2
    
    @property
    def transmittance(self):
        return abs(1/self.__tm[0,0])**2

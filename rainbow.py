import numpy as np

e_0=8.85418782e-12
mu_0=1.25663706e-6
nn_0=np.sqrt(e_0* mu_0)

class Ambient(object):
    def __init__(self, e_r=1, mu_r=1, name=''):
        self.__name=name
    
        self.__e_r=np.array(e_r)
        if isinstance(e_r, (int, float, complex)) and isinstance(mu_r, (int, float, complex)):
            self.__e_r=np.array((e_r,))
            self.__mu_r=np.array((mu_r,))
        elif isinstance(e_r, (tuple, list)) and isinstance(mu_r, (tuple, list)):
            if len(e_r)!=len(mu_r):
                raise ValueError('# of elements contained by e_r and mu_r must be equal')
            else:
                self.__mu_r=np.array(mu_r)

        else:
            raise TypeError('e_r and mu_r both must be an iterable or a number')
  
    @property    
    def info(self):
        return self.__e_r, self.__mu_r, self.__name
    
    @property     
    def depth(self):
        return len(self.__e_r)

    def __repr__(self):
        return f'Ambient:{self.__name} {self.__e_r} {self.__mu_r}'

class ThinLayer(object):
    def __init__(self, thickness, e_r=1, mu_r=1, name=''):
        self.__name=name
        self.__d=thickness
        self.__e_r=np.array(e_r)
        self.__mu_r=np.array(mu_r)
        if isinstance(e_r, (int, float, complex)) and isinstance(mu_r, (int, float, complex)):
            self.__e_r=np.array((e_r,))
            self.__mu_r=np.array((mu_r,))
        elif isinstance(e_r, (tuple, list)) and isinstance(mu_r, (tuple, list)):
            if len(e_r)!=len(mu_r):
                raise ValueError('# of elements contained by e_r and mu_r must be equal')
            else:
                self.__mu_r=np.array(mu_r)

        else:
            raise TypeError('e_r and mu_r both must be an iterable or a number')

    @property        
    def depth(self):
        return len(self.__e_r)
    @property    
    def info(self):
        return self.__d, self.__e_r, self.__mu_r, self.__name
    
    def __repr__(self):
        return f'{self.__name} {self.__d*1e9}nm {self.__e_r} {self.__mu_r}'


class Substrate(object):
    def __init__(self, e_r=1, mu_r=1, name=''):
        self.__name=name
        self.__e_r=np.array(e_r)

        if isinstance(e_r, (int, float, complex)) and isinstance(mu_r, (int, float, complex)):
            self.__e_r=np.array((e_r,))
            self.__mu_r=np.array((mu_r,))
        elif isinstance(e_r, (tuple, list)) and isinstance(mu_r, (tuple, list)):
            if len(e_r)!=len(mu_r):
                raise ValueError('# of elements contained by e_r and mu_r must be equal')
            else:
                self.__mu_r=np.array(mu_r)

        else:
            raise TypeError('e_r and mu_r both must be an iterable or a number')

    @property    
    def info(self):
        return self.__e_r, self.__mu_r, self.__name
    
    @property
    def depth(self):
        return len(self.__e_r)

    def __repr__(self):
        return f'Substrate:{self.__name} {self.__e_r} {self.__mu_r}'
    

class Stack(object):
    def __init__(self):
        self.__ambient=False
        self.__layers=[]
        self.__global_depth=0
        self.__substrate=False
        self.__t=None
        self.__r=None
        self.__transfer_matrix=None
        self.__n_a=None
    def add_layer(self, arg):
        if isinstance(arg, (tuple, list)):
            for ly in arg:
                self.add_layer(ly)
        elif isinstance(arg, ThinLayer):
            if not(self.__global_depth and arg.depth):
                self.__global_depth=arg.depth
            if self.__global_depth==arg.depth:
                self.__layers.append(arg)
            else:
                raise ValueError(f'Depth of {arg.info[3]} layer must be equal to others')
        else:
            raise TypeError('Only Thin Layers can be added into the Stack')
    
    @property    
    def stack(self):
        return self.__ambient,self.__layers,self.__substrate
    

    def add_substrate(self,arg):
        if isinstance(arg, Substrate):
            if not(self.__global_depth and arg.depth):
                self.__global_depth=arg.depth
               
            if arg.depth==self.__global_depth:
                self.__substrate=arg
            else:
                raise ValueError('Added Substrate must have the same depth as others')

        else:
            raise TypeError('An ambient must be a Substrate type')


    def add_ambient(self, arg):
        if isinstance(arg, Ambient):
            if not(self.__global_depth and arg.depth):
                self.__global_depth=arg.depth
               
            if arg.depth==self.__global_depth:
                self.__ambient=arg
                self.__n_a=arg.info[0]*arg.info[1]
            else:
                raise ValueError('Added Ambient must have the same depth as others')

        else:
            raise TypeError('An ambient must be an Ambient type')
    def Radiation(self, wavelenght, theta=0, polarisation_mode='TM'):
        if polarisation_mode=='TE':
            pm=0
        elif polarisation_mode=='TM':
            pm=1
        else:
            raise ValueError('Polarization mode must be string of "TE" or "TM"')
        
        self.__radiation = np.math.pi*2/wavelenght, theta, pm #wavenumber, theta, polarisaton_mode

    @property
    def reflectance(self):
        return self.__r

    @property
    def transmittance(self):
        return self.__t
    
    @property
    def transfer_matrix(self):
        return self.__transfer_matrix

    def render(self):
        _0=self.__ambient.info
        Z_0=np.sqrt(_0[1]/_0[1])
        self.__transfer_matrix=self.__tmgen(0)
        for i in range(1, len(self.__layers)):
            self.__transfer_matrix=self.__ddp(self.__transfer_matrix,self.__tmgen(i))

        gamma_a=np.sqrt(self.__n_a)*nn_0*np.cos(self.__radiation[1])
        n_s=np.sqrt(self.__substrate.info[0]*self.__substrate.info[1])
        gamma_s=n_s*nn_0*np.sqrt(1-(self.__n_a/n_s*np.sin(self.__radiation[1]))**2)

        tm=self.transfer_matrix
        self.__t=2*gamma_a/(gamma_a*tm[0][0]+gamma_a*gamma_s*tm[0][1]+tm[1][0]+gamma_s*tm[1][1])
        self.__r=(gamma_a*tm[0][0] + gamma_a*gamma_s*tm[0][1] - tm[1][0] - gamma_s*tm[1][1])/(gamma_a*tm[0][0]+gamma_a*gamma_s*tm[0][1] + tm[1][0] + gamma_s*tm[1][1])
    
    def __tmgen(self, i):#transfer matrix generator of 'i'th layer
        layer=self.__layers[i].info
        n_i=np.sqrt(layer[1]*layer[2])
        cos_theta_i=np.sqrt(1-(self.__n_a/n_i*np.sin(self.__radiation[1]))**2)
        delta_i=self.__radiation[0]*n_i*layer[0]*cos_theta_i
        gamma_i=n_i*nn_0*cos_theta_i
        return np.array([[np.cos(delta_i), np.sin(delta_i)*1j/gamma_i],[1j*gamma_i*np.sin(delta_i), np.cos(delta_i)]])


    @staticmethod
    def __ddp(A, B):#deep dot product
        C00=A[0][0]*B[0][0] + A[0][1]*B[1][0]
        C01=A[0][0]*B[0][1] + A[0][1]*B[1][1]
        C10=A[1][0]*B[0][0] + A[1][1]*B[1][0]
        C11=A[1][0]*B[0][1] + A[1][1]*B[1][1]
        return np.array([[C00, C01], [C10, C11]])

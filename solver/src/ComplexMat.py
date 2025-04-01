import numpy as np

class ComplexMat:
    def __init__(self, re, im):
        self.re = np.array(re, dtype=np.float64)
        self.im = np.array(im, dtype=np.float64)

    def magnitude(self):
        return np.sqrt(self.re**2 + self.im**2)  # Module |re + i*im|

    def phase(self):
        return np.angle(self.re + 1j * self.im)  # Phase arg(re + i*im)

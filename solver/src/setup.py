import numpy
from setuptools import setup, Extension

module1 = Extension('_solver',
                    include_dirs = ['../include/armanpy/', numpy.get_include()],
                    libraries = ['m', 'z', 'armadillo'],
                    sources = ['solver.i', '../src/solver.cpp'],
                    swig_opts = ["-c++", "-Wall", "-I.", "-I../include/armanpy/"])

setup( name='solver',
       version='1.0',
       ext_modules=[module1],
       install_requires=['numpy', 'matplotlib', 'swig', 'setuptools'],
)
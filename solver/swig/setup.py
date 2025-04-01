from setuptools import setup, Extension

module1 = Extension('_solver', sources=['solver.i', '../src/solver.cpp', '../src/complexmat.cpp'], swig_opts=["-c++"])

setup(name='package_solver',
      py_modules=['solver'],
      version='1.0',
      description="This package implements the solver's functions",
      ext_modules=[module1])

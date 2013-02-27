from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("tools",["tools.pyx"]), Extension("popCSV", ["popCSV.pyx"])]

setup(
  name = 'csv',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
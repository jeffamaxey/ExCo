
# "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat" amd64 / x86
# python setup.py build_ext --inplace

import os
from distutils.core import setup, Extension

items = os.listdir("nimcache/")
nim_c_files = [f"nimcache/{i}" for i in items if i.endswith(".c")]
nim_lexers = Extension(
    'nim_lexers', 
    nim_c_files,
    extra_compile_args = [
        "-Inimcache",
        "-IC:\\Nim\\lib",
    ],
)

# run the setup
setup(ext_modules=[nim_lexers])
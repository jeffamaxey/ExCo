
import os
import subprocess
import shutil
import platform

current_platform = platform.system()

commands = []
if current_platform == "Windows":
    
    commands.extend(
        (
            'CALL "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Auxiliary/Build/vcvars64.bat"',
            'C:\\Nim\\bin\\nim.exe cc --compileOnly --cc:vcc -d:py3_version=3.7 -d:py3_static --noLinking --header:nim_lexers.h nim_lexers.nim',
            'python setup.py build_ext --inplace',
        )
    )
    p = subprocess.Popen(" & ".join(commands), shell=True)
    p.wait()

else:
    
    commands.extend(
        (
            'nim cc --app:lib --compileOnly --cc:gcc -d:py3_version=3.5 -d:py3_static --noLinking --header:nim_lexers.h nim_lexers.nim',
            'python3 setup.py build_ext --inplace',
        )
    )
    for c in commands:
        os.system(c)
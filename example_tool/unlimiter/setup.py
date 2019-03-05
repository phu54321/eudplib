# distutils setup file

import os
import sys

from cx_Freeze import Executable, setup

eudplibPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "eudplib"],
    "include_msvcr": True,
    "include_files": [
        eudplibPath + "/eudplib/core/mapdata/StormLib32.dll",
        eudplibPath + "/eudplib/epscript/libepScriptLib.dll",
    ],
    "excludes": ["tkinter"],
    "optimize": 2,
    "zip_include_packages": "*",
    "zip_exclude_packages": ""
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

setup(name="SC Unlimiter",
      version="0.2",
      description="My GUI application!",
      options={"build_exe": build_exe_options},
      executables=[Executable("unlimiter.py", base=base)]
)

# add SFmpq32.dll manually

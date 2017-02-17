import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"include_files": ["logo.png"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Latitude",
        version = "1.0",
        description = "Infinirun",
        options = {"build_exe": build_exe_options},
        executables = [Executable("latitude.py", base=base, icon="logo.ico")])

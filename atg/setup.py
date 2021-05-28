import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
# buildOptions = dict(
#     packages=['win32api', 'win32con', 'win32gui_struct', 'winxpgui', 'win32gui', 'threading', 'queue', 'PySide6', 'datetime', 'time',
#               'sys', 'os', 'win32print', 'requests', 'itertools', 'glob', 'socket', 'json', 'webbrowser', 'traceback', 'logging', 'idna'],
#     excludes=[],
#     # includes=['Lib/PAConfig', 'Lib/PASocketClient', 'Lib/SysTrayIconModule'],
#     include_files=['icon.ico', 'gui/',
#                    'generator/', 'middleware/', 'techniques/', 'mockapp/']
# )

base = 'Win32GUI' if sys.platform == 'win32' else None

files = ['icon.ico', 'gui/', 'generator/', 'middleware/', 'techniques/', 'mockapp/']

# TARGET
executables = [
    Executable(
        script='main.py',
        base=base,
        targetName='atg.exe',
        icon='./icon.ico',

        # shortcutName=appName,
        # shortcutDir="MyProgramMenu",
    )
    #Executable('main.py', base=base, targetName=appName + ".exe", icon="printadapt.ico")
]

# SETUP CX FREEZE
setup(
    name="atg",
    version="0.0.6",
    description="Automatic Test Generator for Python",
    author="Lampros Karseras",
    options={'build_exe': {'include_files': files}},
    executables=executables

)

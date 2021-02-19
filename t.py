# @Author: Lampros.Karseras
# @Date:   14/01/2021 21:26
import distutils.sysconfig as sysconfig
import os


def std_modules():
    ret_list = []
    std_lib = sysconfig.get_python_lib(standard_lib=True)
    for top, dirs, files in os.walk(std_lib):
        for nm in files:
            if nm != '__init__.py' and nm[-3:] == '.py':
                ret_list.append(os.path.join(top, nm)[len(std_lib) + 1:-3].replace('\\', '.'))
    return ret_list


l = std_modules()
mods = ["inspect",
        "random",
        "sys",
        "traceback",
        "types",
        "pathlib",
        "inspect",
        "random",
        "collections",
        "functools",
        "itertools"
        ]
print([x for x in mods if x not in l])
print("os" in l)

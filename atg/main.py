# @Author: Lampros.Karseras
# @Date:   16/11/2020 10:25
from __future__ import absolute_import

import atg
from atg.core import ATG
import random
import yaml
import inspect
import os
import atg.loader as loader
from collections import OrderedDict
from atg.generator.default_generator import DefaultGenerator
from atg.generator.alt_generator import Alt_Generator
from pathlib import Path
import ast


# parsed_pairs = {}
#
#
# def parseCode(file):
#     with open(file=file) as f:
#         tree = ast.parse(f.read())
#
#     for node in ast.walk(tree):
#         if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
#             docstring = ast.get_docstring(node)
#             if docstring and 'eq' in docstring:
#                 parsed_pairs[node.name] = ''.join(
#                     [x.split(':eq:')[1].strip() for x in docstring.split('\n') if 'eq' in x]).split(', ')

def main():
    if os.path.exists('config.yml'):
        with open('config.yml', 'r') as conf:
            try:
                atg_config = yaml.safe_load(conf)
            except yaml.YAMLError as e:
                print(e)
                return "Couldn't load configuration :: config.yml"
        if atg_config is None:
            atg_config = {}

        if not isinstance(atg_config, dict):
            return "Couldn't load configuration :: config.yml"

        print(atg_config)

        if 'file_path' not in atg_config:
            return 'Filepath to module must be provided!'
        file_path = atg_config.pop('file_path')
        os.chdir(Path(file_path).parent)
        print(file_path)
        print(atg_config)

        with open(file_path) as file:
            node = ast.parse(file.read())

        functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        classes = [n for n in node.body if isinstance(n, ast.ClassDef)]

        ATG(config=atg_config, file_path=file_path, classes=classes, functions=functions,
            generator=Alt_Generator()).run()


# def _getModule(mod):
#     path_to_dir = (Path(__file__).parent / self._config_file).resolve().parent
#     module_name = (path_to_dir / self._config[mod]['file_path']).resolve()
#     return module_name


if __name__ == '__main__':
    os.chdir('../mockapp')
    main()

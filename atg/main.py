# @Author: Lampros.Karseras
# @Date:   16/11/2020 10:25
import ast
import random
import yaml
import inspect
import os
from techniques.partitioning import createPartitions

parsed_pairs = {}


def parseCode(file):
    with open(file=file) as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
            docstring = ast.get_docstring(node)
            if docstring and 'eq' in docstring:
                parsed_pairs[node.name] = ''.join(
                    [x.split(':eq:')[1].strip() for x in docstring.split('\n') if 'eq' in x]).split(', ')


class ATG:
    def __init__(self, config_file):
        import initializelogging
        initializelogging.setUpLogging()
        import logging
        self.logger = logging.getLogger(__name__)
        self._config_file = config_file
        self._caller = inspect.stack()[1][1]
        self.logger.info(self._caller)
        self._config = self._getConfiguration()
        self.logger.info('Initialized ATG')

    def _getConfiguration(self):
        with open(self._config_file, 'r') as s:
            try:
                return yaml.safe_load(s)
            except yaml.YAMLError as e:
                print(e)

    def _getModule(self, mod):
        from pathlib import Path
        path_to_dir = (Path(__file__).parent / self._config_file).resolve().parent
        module_name = (path_to_dir / self._config[mod]['file_path']).resolve()
        return module_name

    def run(self):
        for mod in self._config.keys():
            module = self._getModule(mod)
            partitions = createPartitions(self._config[mod]['partitions'], self._config[mod]['invalid_choices'])
            # TODO: Apply BlackBox techniques. Seperate file
            # TODO: Get the return and push it to test generator
            return module, partitions


if __name__ == '__main__':
    atg = ATG("../mockapp/config.yml")
    # parseCode(atg.run())

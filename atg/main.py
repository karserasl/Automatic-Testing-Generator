# @Author: Lampros.Karseras
# @Date:   16/11/2020 10:25
import ast
import random
import yaml
import inspect
import os


def getEqPartitions(x):
    result = []
    for part in x.split(','):
        if '-' in part:
            a, b = part.split('-')
            a, b = int(a), int(b)
            result.append(random.choice(range(a, b + 1)))
        else:
            a = int(part)
            result.append(a)

    return result


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
        with open(self._config_file, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def _getModule(self):
        from pathlib import Path
        path_to_dir = (Path(__file__).parent / self._config_file).resolve().parent
        modulename = (path_to_dir / self._config['test_config']['file_path']).resolve()
        return modulename

    def run(self):
        module = self._getModule()
        # TODO: Apply BlackBox techniques. Seperate file
        # TODO: Get the return and push it to test generator
        pass

if __name__ == '__main__':
    atg = ATG("../mockapp/config.yml")

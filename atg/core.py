# @Author: Lampros.Karseras
# @Date:   10/01/2021 00:43
import ast
import inspect
from collections import OrderedDict
from atg.generator.default_generator import DefaultGenerator
import loader
import initializelogging
import logging

initializelogging.setUpLogging()
logger = logging.getLogger(__name__)


class ATG:

    def __init__(self, config, file_path, classes=None, functions=None, generator=None, mocks_subs=None,
                 extra_imports=None):

        self._config = config
        self._classes = classes
        self._functions = functions
        self._file_path = file_path
        self._caller = inspect.stack()[1][1]
        logger.info(self._caller)
        logger.info('Initialized ATG')
        self._techniques = loader.getAllTechniques()
        self._generator = generator or DefaultGenerator()
        # self._generator.set_mock_substitutes(mocks_subs or {})
        # self._generator.set_extra_imports(extra_imports or {})

    def find(self, key, dictionary):
        # everything is a dict
        for k, v in dictionary.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in self.find(key, v):
                    yield result

    def getPartitions(self, variables):
        partitions = {}
        for arg, value in variables.items():
            if isinstance(value, dict):
                if 'partitions' in value:
                    partitions[arg] = self._techniques['partitioning'].run(value['partitions'],
                                                                           value['invalid_choices'])
        return partitions

    def run(self):
        # TODO: Apply BlackBox techniques. Seperate file
        # TODO: Get the return and push it to test generator
        # for f in self._functions:
        #     variables_values = self.findValues(f.name)

        for cls in self._classes:
            methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
            for method in methods:
                # show_info(method)
                variables_values = self.findValues(method.name)
                if variables_values:
                    if recursive_lookup('partitions', variables_values):
                        # TODO: Pass partitions to generator to dump partition tests to new file
                        partitions = self.getPartitions(variables_values)
                        print(partitions)
                    if recursive_lookup('combinations', variables_values):
                        # TODO: Ask for results of each pairwise combination
                        pass
                    if recursive_lookup('value', variables_values):
                        # TODO: Pass variables_values to generator
                        pass
                test = self._generator.dump(self._file_path, method, cls, partitions)
                print(test)
        # if 'combinations' in self._config[cls]:
        #     pairwise = self._techniques['pairwise']
        #     for i, pairs in enumerate(pairwise.Pairwise(OrderedDict(self._config[cls]['combinations']))):
        #         print("{:2d}: {}".format(i, pairs))
        # functions = self._config[cls]['function']
        # test = self.dump(filename=module, functions=functions)

    def findValues(self, func):
        for s in find(func, self._config):
            return s

    def dump(self, filename, functions):
        return self._generator.dump(filename, functions)


def show_info(functionNode):
    print("Function name:", functionNode.name)
    print("Args:")
    for arg in functionNode.args.args:
        # import pdb; pdb.set_trace()
        print("\tParameter name:", arg.arg)


def find(key, dictionary):
    # everything is a dict
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result


def recursive_lookup(k, d):
    if k in d:
        return d[k]
    for v in d.values():
        if isinstance(v, dict):
            return recursive_lookup(k, v)
    return None

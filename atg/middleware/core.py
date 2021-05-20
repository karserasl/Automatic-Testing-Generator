# @Author: Lampros.Karseras
# @Date:   10/01/2021 00:43
import ast
import inspect
import logging

from middleware import loader
from middleware import initializelogging
from generator.default_generator import DefaultGenerator

initializelogging.setup_logging()
logger = logging.getLogger(__name__)


class ATG:

    def __init__(self, generator=None):

        self._analyzed_data = {}
        self._func_params = {}
        self._processed_output = {}
        self._selected_function = None
        self._file_path = None
        self._file_node = None
        self._techniques = loader.get_all_techniques()
        self._generator = generator or DefaultGenerator()
        logger.info('Initialized ATG')

    def find(self, key, dictionary):
        # everything is a dict
        for k, v in dictionary.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in self.find(key, v):
                    yield result

    def run(self, outputs: list, inv_choice, pairwise):
        print(outputs, inv_choice)  # TODO: Remove this
        if not pairwise:
            for tech_id, technique in self._techniques.items():
                if not tech_id == 'pairwise':
                    self._processed_output[tech_id] = technique.run(outputs, inv_choice)
                    print(self._processed_output)
        else:
            return self._techniques['pairwise'].run(outputs)

        return True

    def check_if_exists(self):
        return False

    def analyse_file(self, filepath):
        self._file_path = filepath
        try:
            with open(self._file_path) as f:
                self._file_node = ast.parse(f.read())
        except Exception as e:
            logger.error(f'Error reading py file :: {e}')

        logger.info(self._file_path)
        functions = [n for n in self._file_node.body if isinstance(n, ast.FunctionDef)]
        classes = [n for n in self._file_node.body if isinstance(n, ast.ClassDef)]
        if classes:
            for i, cls in enumerate(classes):
                cls_name = cls.name
                methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
                self._analyzed_data[f'{cls_name}'] = [method.name for method in methods if
                                                      not method.name.startswith('__init')]
                for method in methods:
                    if not method.name.startswith('__init'):
                        self._func_params[method.name] = self.get_functions_parameters(method)
                        # show_info(method)

        if functions:
            self._analyzed_data['Functions'] = [func.name for func in functions if not func.name.startswith('__init')]
            for func in functions:
                if not func.name.startswith('__init'):
                    self._func_params[func.name] = self.get_functions_parameters(func)
                    # show_info(func)

    @staticmethod
    def get_functions_parameters(function):
        return [arg.arg for arg in function.args.args if not arg.arg.startswith('self')]

    @property
    def get_data(self):
        self.clean_analyzed_data()
        print(self._func_params)

        check = bool({k: v for k, v in self._analyzed_data.items() if v})
        return self._analyzed_data if check else None

    @property
    def get_params(self):
        self.clean_analyzed_data()
        return self._func_params

    def set_sel_function(self, value):
        if value:
            self._selected_function = value

    def clean_analyzed_data(self):
        self._func_params = {k: v for k, v in self._func_params.items() if v}
        self._analyzed_data = {k: list(set(v).intersection(self._func_params.keys())) for k, v in
                               self._analyzed_data.items()}

    @staticmethod
    def get_default_args(func):
        signature = inspect.signature(func)
        return {
            k: v.default
            if v.default is not inspect.Parameter.empty else None
            for k, v in signature.parameters.items()
        }

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

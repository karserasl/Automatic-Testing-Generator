# @Author: Lampros.Karseras
# @Date:   11/01/2021 20:34
import logging
import sys
from copy import deepcopy
import itertools
from copy import copy

logger = logging.getLogger(__name__)


class TestsGenerator:

    def __init__(self):
        self._output = []
        self._imports = {('unittest',)}
        self._count = 0

    def _set_extra_imports(self, imports):
        for imp in imports:
            self._imports.add(imp)

    def dump(self, filename, method, processed_output, cls):
        copy_output = deepcopy(processed_output)
        print(cls)
        self._dump_tests(filename, method, cls, copy_output)
        for line in open(filename):
            line = line.replace('\n', '')
            if line.startswith('import '):
                self._add_import(line.replace('import ', ''))
            if line.startswith('from '):
                module = line.replace('from ', '').split(' import')[0]
                imports = [import_.strip() for import_ in line.split('import ')[1].split(',')]
                for import_ in imports:
                    self._add_import(module, import_)
        return '\n'.join([*self._style_imports(), *self._output]), self._count

    def _style_imports(self):
        imports = sorted(self._imports)
        if ('atg',) in imports:
            imports.remove(('atg',))

        def _format(import_items):
            if len(import_items) == 2:
                if import_items != '__main__':
                    return f'from {import_items[0]} import {import_items[1]}'
            return f'import {import_items[0]}'

        return list(map(_format, imports))

    def _dump_tests(self, filename: str, method: str, cls: str, copy_output: dict):
        self._output.append('')
        self._output.append('')
        cls_definition = None
        if cls:
            cls_definition = f'self.{cls.lower()}'
            self._output.append(f'class {cls}(unittest.TestCase):')
            self._output.append(f"""
            {self.indent(1)}def setUp(self) -> None:\n
            {self.indent(2)}{cls_definition}={self._get_module_name(filename)}.{cls}()
            """)
        logger.info(cls)
        self._output.append(
            f"""
            {self.indent(1)}# -------- {method.upper()} -------- #
            """
        )

        counter = itertools.count()

        for technique, result_lst in copy_output.items():
            if not result_lst:
                continue
            for result in result_lst:
                expected_ans = result.pop()
                for inputs in result:
                    self._output.append(f'{self.indent(1)}def test_{method}_{next(counter)}(self):\n')
                    if cls_definition:
                        self._output.append(
                            f"""
                            {self.indent(2)}self.assertEqual(\n
                            {self.indent(3)}{cls_definition}.{method}({inputs}),\n
                            {self.indent(3)}{expected_ans}
                            """
                        )
                    else:
                        self._output.append(
                            f"""
                            {self.indent(2)}self.assertEqual(\n
                            {self.indent(3)}{method}({inputs}),\n
                            {self.indent(3)}{expected_ans}
                            """
                        )
                    self._count = next(copy(counter))

        self._output.append('if __name__ == "__main__":')
        self._output.append(f'{self.indent(1)}unittest.main()\n')

    def _add_import(self, module_name, part_name=None):

        if part_name:
            if module_name in sys.modules:
                mod = sys.modules[module_name]
                if not hasattr(mod, part_name):
                    return
        self._imports.add((module_name, part_name) if part_name else (module_name,))

    @staticmethod
    def _shorten_filename(filename):
        return filename.split('/')[-1].split('\\')[-1]

    def _get_module_name(self, filename):
        return self._shorten_filename(filename).replace(".py", "").replace("/", ".")

    @staticmethod
    def indent(n):
        return '    ' * n

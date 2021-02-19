# @Author: Lampros.Karseras
# @Date:   11/01/2021 20:34

import inspect
import random
import sys
import traceback
import types

from atg import runtime


def indent(n):
    return '    ' * n


class Alt_Generator:
    def __init__(self):
        self.output_ = []
        self.imports_ = {('unittest',)}
        self.instances = {}

    def set_extra_imports(self, imports):
        for imp in imports:
            self.imports_.add(imp)

    def dump(self, filename, method, cls=None, partitions=None):
        self.output_ = []
        self.dump_tests(filename, method, cls, partitions)
        for line in open(filename):
            line = line.replace('\n', '')
            if line.startswith('import '):
                self.add_import(line.replace('import ', ''))
            if line.startswith('from '):
                module = line.replace('from ', '').split(' import')[0]
                imports = [import_.strip() for import_ in line.split('import ')[1].split(',')]
                for import_ in imports:
                    self.add_import(module, import_)
        return '\n'.join(self.format_imports() + self.output_)

    def format_imports(self):
        imports = sorted(self.imports_)
        if ('atg',) in imports:
            imports.remove(('atg',))

        def format(imp):
            if len(imp) == 2:
                if imp != '__main__':
                    return 'from %s import %s' % (imp[0], imp[1])
            return 'import %s' % imp[0]

        return list(map(format, imports))

    def collect_instances(self, method):
        for code, function in filter(lambda fn: runtime.get_code_name(fn[0]) == '__init__', method):
            for _, calls in function.calls.items():
                for (args, _) in calls[:1]:
                    func_self = args['self']
                    func_self_type = func_self.__class__
                    for base in func_self.__class__.__bases__:
                        for _, init in filter(lambda member: member[0] == '__init__', inspect.getmembers(base)):
                            if getattr(init, "__code__", None) == code:
                                func_self_type = base
                    mod = func_self_type.__module__
                    self.add_import(mod, func_self_type.__name__)
                    self.instances[self.get_object_id(type(func_self), func_self)] = (
                        func_self_type.__name__, code, args)

    def find_module(self, code):
        for modname, mod in sys.modules.items():
            file = getattr(mod, '__file__', '').replace('.pyc', '.py')
            if file == runtime.get_code_filename(code):
                if modname == "__main__":
                    modname = file.replace(".py", "").replace("/", ".")
                self.add_import(modname)
                return modname, mod

    def get_defining_item(self, code):
        filename = runtime.get_code_filename(code)
        lineno = runtime.get_code_lineno(code)
        modname, mod = self.find_module(code)
        for _, clazz in inspect.getmembers(mod, predicate=inspect.isclass):
            for _, member in inspect.getmembers(clazz, predicate=inspect.ismethod):
                member_code = runtime.get_code(member)
                member_filename = runtime.get_code_filename(member_code)
                member_lineno = runtime.get_code_lineno(member_code)
                if filename == member_filename and lineno == member_lineno:
                    self.add_import(modname, clazz.__name__)
                    return clazz, member
            for _, member in inspect.getmembers(clazz, predicate=lambda member: isinstance(member, property)):
                self.add_import(modname, clazz.__name__)
                return clazz, member
            for _, member in inspect.getmembers(clazz, predicate=inspect.isfunction):
                member_code = runtime.get_code(member)
                member_filename = runtime.get_code_filename(member_code)
                member_lineno = runtime.get_code_lineno(member_code)
                if filename == member_filename and lineno == member_lineno:
                    self.add_import(modname, clazz.__name__)
                    return clazz, member
            for _, member in inspect.getmembers(mod, predicate=inspect.isfunction):
                # Module-level function support, note the difference in return statement
                member_code = runtime.get_code(member)
                member_filename = runtime.get_code_filename(member_code)
                member_lineno = runtime.get_code_lineno(member_code)
                if filename == member_filename and lineno == member_lineno:
                    self.add_import(modname, clazz.__name__)
                    return mod, member
        if modname != '__main__':
            self.add_import(modname)
        return mod, mod

    def dump_create_instance(self, typename):
        self.output_.append(
            indent(2) + '%s_instance = %s()' % (typename.lower(), typename))

    def get_instance(self, instances, func_self):
        _type = type(func_self)
        return instances.get(self.get_object_id(_type, func_self)) or (func_self.__class__.__name__, _type, {})

    def dump_call(self, filename, code, call):
        definer, member = self.get_defining_item(code)
        for (args, return_value) in call:
            func_self = args.get('self')
            is_func = inspect.isfunction(member)
            is_method = inspect.ismethod(member)
            is_static = isinstance(definer.__dict__.get(runtime.get_code_name(code)), staticmethod)
            is_mod = isinstance(definer, types.ModuleType)
            if isinstance(member, property) or inspect.ismethod(member):
                if not is_static:
                    typename, init, init_args = self.get_instance(self.instances, func_self)
                    if typename == "NoneType":
                        self.output_.append(''.join([
                            indent(2),
                            'pass\n\n'
                        ]))
                        continue
                    self.dump_create_instance(typename)
                    if 'self' in args:
                        del args['self']
                    target = '%s_instance' % typename.lower()
                else:
                    target = definer.__name__
            else:
                self.add_import(filename)
                target = definer.__name__

            # Useful for debugging
            # print '-' * 80
            # print 'call:   ', call
            # print 'definer:', definer
            # print 'member: ', member
            # print 'target: ', target
            # print 'name:   ', runtime.get_code_name(code)
            # print 'ismod?: ', is_mod
            # print 'static?:', is_static
            # print 'method?:', is_method
            # print 'func?:  ', is_func
            # print '-' * 80

            call = '%s.%s' % (target, runtime.get_code_name(code))
            if is_method or is_func or is_static or is_mod:
                call += '(%s)' % (
                    ','.join(['%s=%s' % (k, repr(v)) for k, v in args.items()]),
                )
            call += ',\n'
            self.output_.append(''.join([
                indent(2),
                'self.assert%s(\n' % self.get_assert(return_value),
                indent(3),
                call,
                indent(3),
                '%s\n' % self.get_assert_value(return_value),
                indent(2),
                ')\n'
            ]))
            self.output_.append('')
            break

    def dump_tests(self, filename, method, cls, partitions):
        self.output_.append('')
        self.output_.append('')
        if cls:
            self.output_.append(f'class {cls.name}(unittest.TestCase):')
            self.output_.append(
                indent(1) + 'def setUp(self) -> None:\n' +
                indent(2) + f'self.{cls.name.lower()}={self.get_module_name(filename)}.{cls.name}()'
            )

        import itertools
        counter = itertools.count().__next__

        if partitions:
            for arg, partition in partitions.items():
                self.output_.append(indent(1) + f'def test_{method.name}_{counter()}(self):')
                # try:
                #     self.dump_call(filename, code, random.choice(list(function.calls.values())))
                # except:
                #     traceback.print_exc()

        self.output_.append('if __name__ == "__main__":')
        self.output_.append(indent(1) + 'unittest.main()\n')

    def add_import(self, module_name, part_name=None):

        if part_name:
            if module_name in sys.modules:
                mod = sys.modules[module_name]
                if not hasattr(mod, part_name):
                    return
        self.imports_.add((module_name, part_name) if part_name else (module_name,))

    @staticmethod
    def get_filename(code):
        return Alt_Generator.shorten_filename(runtime.get_code_filename(code))

    @staticmethod
    def shorten_filename(filename):
        return filename.split('/')[-1].split('\\')[-1]

    def get_module_name(self, filename):
        return Alt_Generator.shorten_filename(filename).replace(".py", "").replace("/", ".")

    @staticmethod
    def get_lineno(code):
        return code.co_firstlineno

    @staticmethod
    def get_full_class_name(value):
        return value.__class__.__module__ + "." + value.__class__.__name__

    @staticmethod
    def get_assert_value(value):
        value = Alt_Generator.get_full_class_name(value) if Alt_Generator.is_object(value) else repr(value)
        return value.replace("<type '", '').replace("'>", '')

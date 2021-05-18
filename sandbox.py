# @Author: Lampros.Karseras
# @Date:   16/11/2020 10:47
import mockapp.calculator as calc
# from docstring_parser import parse
from parse_docstrings import parse_docstring


def generate_testcase(func):
    def func_wrapper(*args, **kwargs):
        return_value = func(*args, **kwargs)
        print('assert %s(%s) == %s' % (func.__name__, ', '.join(repr(arg) for arg in args), return_value))
        return return_value

    return func_wrapper


@generate_testcase
def square(x):
    return x ** 2


def equivalence_partition(iterable, relation):
    """Partitions a set of objects into equivalence classes

    Args:
        iterable: collection of objects to be partitioned
        relation: equivalence relation. I.e. relation(o1,o2) evaluates to True
            if and only if o1 and o2 are equivalent

    Returns: classes, partitions
        classes: A sequence of sets. Each one is an equivalence class
        partitions: A dictionary mapping objects to equivalence classes
    """
    classes = []
    partitions = {}
    for o in iterable:  # for each object
        # find the class it is in
        found = False
        for c in classes:
            if relation(next(iter(c)), o):  # is it equivalent to this class?
                c.add(o)
                partitions[o] = c
                found = True
                break
        if not found:  # it is in a new class
            classes.append(set([o]))
            partitions[o] = classes[-1]
    return classes, partitions


def equivalence_enumeration(iterable, relation):
    """Partitions a set of objects into equivalence classes

    Same as equivalence_partition() but also numbers the classes.

    Args:
        iterable: collection of objects to be partitioned
        relation: equivalence relation. I.e. relation(o1,o2) evaluates to True
            if and only if o1 and o2 are equivalent

    Returns: classes, partitions, ids
        classes: A sequence of sets. Each one is an equivalence class
        partitions: A dictionary mapping objects to equivalence classes
        ids: A dictionary mapping objects to the indices of their equivalence classes
    """
    classes, partitions = equivalence_partition(iterable, relation)
    ids = {}
    for i, c in enumerate(classes):
        for o in c:
            ids[o] = i
    return classes, partitions, ids


def check_equivalence_partition(classes, partitions, relation):
    """Checks that a partition is consistent under the relationship"""
    for o, c in partitions.items():
        for _c in classes:
            assert (o in _c) ^ (not _c is c)
    for c1 in classes:
        for o1 in c1:
            for c2 in classes:
                for o2 in c2:
                    assert (c1 is c2) ^ (not relation(o1, o2))


def test_equivalence_partition():
    relation = lambda x, y: (x - y) % 4 == 0
    classes, partitions = equivalence_partition(
        range(-3, 5),
        relation
    )
    check_equivalence_partition(classes, partitions, relation)
    for c in classes: print(c)
    for o, c in partitions.items(): print(o, ':', c)


if __name__ == '__main__':
    # print(square(3) + square(4) == square(5))
    # calc.Calculator.uniClassification(51)
    # doc = parse_docstring(calc.Calculator.uniClassification.__doc__)
    # import configparser
    # import os
    #
    # config = configparser.ConfigParser()
    # config.read('./mockapp/input.ini')
    # os.chdir('./mockapp/')
    # sections = config.sections()
    # print(f'Sections: {sections}')
    # for section in sections:
    #
    #     if config.has_section(section):
    #         print(f'Config file has section {section}')
    #
    #     section1 = dict(config[section])
    # import yaml
    #
    # with open("./config.yml", 'r') as stream:
    #     try:
    #         yml = yaml.safe_load(stream)
    #     except yaml.YAMLError as exc:
    #         print(exc)
    # from main import ATG
    #
    # atg = ATG("./mockapp/config.yml").run()
    # parseCode(run())
    # test_equivalence_partition()

    # import yaml
    # with open('./mockapp/config.yaml', 'r') as conf:
    #     try:
    #         a = yaml.safe_load(conf)
    #     except yaml.YAMLError as e:
    #         print(e)
    import loader as l

    iouts = []
    for i in range(100):
        if i % 15 == 0:
            iouts.append(l.parameters(i, '15 mod'))
        if i % 50 == 0:
            iouts.append(l.parameters(i, '50 mod'))
    params = {
        'grade': iouts
    }
    print(params)

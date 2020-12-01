# @Author: Lampros.Karseras
# @Date:   16/11/2020 10:25
import ast
import random


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


def main(file):
    parseCode(file)


if __name__ == '__main__':
    main('../mockapp/calculator.py')

import atg
import foo

test_subjects = [foo.Foo]

extra_imports = [
    ('random', 'random'),
]

with magic(test_subjects, extra_imports=extra_imports, verbose=True):
    foo.main()

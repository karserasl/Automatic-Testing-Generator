import os
import pickle

from pathlib import Path
root = os.path.dirname('./mockapp/calculator.py')
config_file = Path(os.path.normpath(f'{root or "."}/.atg_config'))
if config_file.is_file():
    try:
        with open(config_file, 'rb') as f:
            _selected_function, _processed_output, _selected_cls = pickle.load(f)
    except Exception as e:
        pass
print(_selected_function, _processed_output, _selected_cls)

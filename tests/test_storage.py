import os, tempfile
from modules.storage import load_json_safe

def test_load_safe():
    assert load_json_safe('non_existent.json', {'a': 1}) == {'a': 1}

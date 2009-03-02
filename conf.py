import os
from yaml import load as yaml_load

class Resolver(object):
    def __init__(self, _dict=None):
        self._dict = _dict

    def __repr__(self):
        return repr(self._dict)

    def __getattr__(self, key):
        if key.startswith('_'):
            return super(object, self).__getattr__(key)
        if key in self._dict:
            if isinstance(self._dict[key], dict):
                return Resolver(self._dict[key])
            return self._dict[key]
        return None

class Settings(Resolver):
    """
    server config
    """
    def __init__(self, config_file=None):
        if not config_file:
            config_file = os.path.join(os.path.dirname(
                    os.path.abspath(__file__)), 'app.yaml')
        f = open(config_file, 'r')
        self._yaml = f.read()
        f.close()
        self._dict = yaml_load(self._yaml)

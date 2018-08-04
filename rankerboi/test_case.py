from ast import literal_eval

_namespace = {}

def _get_test_case_name():
    i = 0
    test_name = 'TestCase#' + str(i)
    while test_name in _namespace:
        i += 1
        test_name = 'TestCase#' + str(i)
    return test_name


class TestCase(object):

    def __init__(self, input, output, timeout=None, name=None):
        self._check_dtypes(input)
        self._check_dtypes(output)
        self.input = input
        if output == 'error':
            raise ValueError('Reserrved token : ' + output)
        self.output = output
        self.timeout = timeout
        self._original_name = name
        if name is None:
            name = _get_test_case_name()
        else:
            if name in _namespace:
                raise Exception('Another test with name ' + name + ' already exists.')
        _namespace[name] = self
        self.name = name

    def serialize(self):
        config = {}
        config['input'] = self.input
        config['output'] = self.output
        config['timeout'] = self.timeout
        config['name'] = self._original_name
        return config

    def _check_dtypes(self, x):
        if type(x) == str:
            return True
        try:
            assert literal_eval(str(x)) == x
        except ValueError:
            raise ValueError('Only basic python types such as int, float, str, tuple, list and dict are allowed.')

    @classmethod
    def deserialize(cls, config):
        return cls(**config)
from .test_case import TestCase
from .executioner import execute
from time import time
import inspect
import timeit

def _str(x):
    if type(x) is str:
        return '\'' + x + '\''

class Challenge(object):

    def __init__(self, name=None, description='', input_var_name=None, output_var_name=None, method_name=None, timeout=None):
        self.name = name
        self.description = description
        self.test_cases = []
        if method_name:
            assert not output_var_name, 'Both output_var_name and method_name were specified.'
        else:
            assert None not in [input_var_name, output_var_name], 'Either input_var_name and output_var_name or method_name should be specified.'
        self.input_var_name = input_var_name
        self.output_var_name = output_var_name
        self.method_name = method_name
        self.timeout = None

    def serialize(self):
        config = {}
        config['name'] = self.name
        config['description'] = self.description
        config['timeout'] = self.timeout
        config['test_cases'] = [tc.serialize() for tc in self.test_cases]
        return config

    @classmethod
    def deserialize(cls, config):
        tcs = config.pop('test_cases')
        challenge = cls(**config)
        deserialize = TestCase.deserialize
        [challenge.add_test_case(deserialize(tc)) for tc in tcs]
        return challenge

    def add_test_case(self, *test_case):
        if len(test_case) == 1:
            assert type(test_case[0]) == TestCase, 'Required TestCase object. Received ' + str(type(test_case[0]))
            test_case = test_case[0]
        else:
            test_case = TestCase(*test_case)
        self.test_cases.append(test_case)

    def _run(self, code, test_case):
        glbls = {}
        input_var_name = self.input_var_name
        output_var_name = self.output_var_name
        method_name = self.method_name
        if input_var_name:
            glbls[input_var_name] = test_case.input
        if output_var_name:
            glbls[output_var_name] = None
            code += '\nglobals()[{}] = {}'.format(output_var_name, output_var_name)
        elif method_name:
            extra_code = """
import inspect
args = inspect.getargspec({}).args
if len(args) == 0:
    globals()['output'] = {}()
elif len(args) == 1:
    globals()['output'] = {}({})
else:
    raise Exception('Invalid method signature.')
"""
            code += '\n'
            code += extra_code.format(method_name, method_name, method_name, _str(test_case.input))
        timeout = self.timeout
        if timeout is None:
            timeout = test_case.timeout
        out_dict, time_taken, timed_out = execute(code, glbls, timeout)
        return out_dict.get('error', False), time_taken, timed_out


        
        

        








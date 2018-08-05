from .test_case import TestCase
from .executioner import execute
from .csv_reader import CSVReader
from .anti_plag import AntiPlag
from .progressbar import ProgressBar
from time import time
import inspect
from csv import writer


def _str(x):
    if type(x) is str:
        return '\'' + x + '\''
    return str(x)

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
        error = None
        if self.output_var_name is not None:
            if self.output_var_name not in out_dict:
                if 'error' not in out_dict:
                    error = 'Out variable not set.'
                out = None
            else:
                out = out_dict[self.output_var_name]
        else:
            out = out_dict.get('output')
        passed = out == test_case.output
        if error is None:
            error = out_dict.get('error', None)
        if error:
            passed = False
        if timed_out:
            passed = False
        return {'test_case': test_case.name, 'passed' : passed, 'time_taken' : time_taken, 'error' : error, 
        'timed_out' : timed_out, 'output' : out, 'expected_output' : test_case.output}


    def run(self, code):
        _run = self._run
        results = []
        pbar = ProgressBar(len(self.test_cases))
        for tc in self.test_cases:
            results.append(self._run(code, tc))
            pbar.update()
        return results

    def run_csv(self, input_file, output_file='results.csv', individual_results=True, anti_plag=True):

        with open(output_file, 'w') as f:
            csv = CSVReader(input_file)
            csv2 = writer(f)
            data = csv.data
            header = csv.header
            header.append('Passed')
            header.append('Run time')
            header.append('Error')
            header.append('Plagiarized')
            csv2.writerow(header)
            csv2.writerow()
            name_col = csv.name_col
            code_col = csv.code_col
            if anti_plag:
                ap = AntiPlag()
                codes = [x[code_col] for x in data]
                ap_results = ap(codes)
                bad_bois = set()
                for group in ap_results:
                    for boi in group:
                        bad_bois.add(boi)
            for i, x in enumerate(data):
                name = x[name_col]
                code = x[code_col]
                print("Running tests for user {} ...".format(name))
                results = self.run(code)
                row = data[i][:]
                is_bad_boi = i in bad_bois
                row.append('Yes')
                if is_bad_boi:
                    row[-1] = 'No'
                else:
                    for tc in results:
                        if not tc['passed']:
                            row[-1] = 'No'
                            break
                row.append(sum([r['time_taken'] for r in results]))
                row.append('')
                for res in results:
                    if res['error'] is None:
                        if res['timed_out']:
                            row[-1] = 'Timed out'
                            break
                    else:
                        row[-1] = res['error']
                if is_bad_boi:
                    row.append('Yes')
                else:
                    row.append('No')
                csv2.writerow(row)

# Rankerboi : Testing, Timing and Anti Plagiarization


--------

The registration process for Kerala AI Initiative events often includes a mini coding challenge, and to keep things simple, the code is entered in the registration form itself (Google Form). This utility let's the Initiative members to test, time and rank the applicants' code and detect plagiarization with ease.

## Installation

```bash
git clone https://www.github.com/keralaai/rankerboi.git
cd rankerboi
python setup.py install
```

## Usage

The central object in rankerboi is a `Challenge`. It defines the rules regarding the input and output.There are 2 kinds of challenges:

* Variable in/Variable out
   -  In a var-in/var-out challenge, the user expects the inputs to be in a given variable, and the user is expected to write the output to another given variable.
   - Example:
   >Write a program to check if a given number is even or odd. If even, output True. Else, output False. Then number will be stored in variable `num`. The output should be saved to variable `out`
   ```python
   challenge = Challenge(input_var_name='num', output_var_name='out')
   ```
   Above challenge will accept the following code:
   ```python
   if num % 2:
        out = False
    else:
        out = True
   ```
  
 
 * Method based challenge
    - In a method based challenge the user is expected to write a function with a given name that accepts the input as a single argument (multiple inputs should be implemented as list/tuple etc) and returns the required output.
Example:
```python
challenge = Challenge(method_name='is_even')
```
Above challenge will accept the following code:

```python
def is_even(x):
    return not(x % 2)
```

Once your `Challenge` object is ready, you can add `TestCase`s to your challenge. A `TestCase` object is basically an input-output pair.

```python
tc1 = TestCase(1, False)
tc2 = TestCase(10, True)
tc3 = TestCase(13, False)

challenge.add_test_case(tc1)
challenge.add_test_case(tc2)
challenge.add_test_case(tc3)
```

Or you can try the less verbose version:

```python
challenge.add_test_case(1, False)
challenge.add_test_case(10, True)
challenge.add_test_case(13, False)
```

Now you can call `challenge.run` on a piece of code and get results.

```python
code = """def is_even(x):return not(x % 2);"""
print(challenge.run(code))
```

Otuptut:
```bash
3/3 [====================================>] - 100%

[{'expected_output': False, 'timed_out': False, 'passed': True, 'error': None, 'output': False, 'time_taken': 0.0, 'test_case': 'TestCase#1'}, 
{'expected_output': True, 'timed_out': False, 'passed': True, 'error': None, 'output': True, 'time_taken': 0.0010001659393310547, 'test_case': 'TestCase#2'},
{'expected_output': False, 'timed_out': False, 'passed': True, 'error': None, 'output': False, 'time_taken': 0.0, 'test_case': 'TestCase#3'}]
```

### Working with Google Forms CSV

Google Forms lets you download the responses as CSV file, which can be read directly from rankerboi:

```python
challenge.run_csv('input.csv', 'output.csv')
```

Here `input.csv` is the file downloaded from Google Forms. Rankerboi will add additional columns such as `Passed`, `Run Time`, `Error` and `Plagiarized` and save the output to `output.csv`.

### Time outs

You can set a global time limit to a challenge using the timeout argument:
```python
challenge = Challenge(method_name='f', timeout=5) ## Max run time 5 seconds.
```
If the user's code takes more than 5 seconds, execution will be terminated.
You can also set timeouts on a per test case basis. Simply set the timeout argument when creating `TestCase` object:

```python
tc1 = TestCase(17, False, timeout=5)
tc2 = TestCase(10000, True, timeout=10)
challenge.add_test_case(tc1)
challenge.add_test_case(tc2)
```

Or,
```python
challenge.add_test_case(17, False, timeout=5)
challenge.add_test_case(10000, True, timeout=10)
```
-----

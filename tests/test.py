from rankerboi import Challenge, TestCase

ch = Challenge(method_name='f')

tc = TestCase(None, 5)

ch.add_test_case(tc)

code ="""def f():
    return 5

"""

ch._run(code, tc)


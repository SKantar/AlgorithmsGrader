from grader.grader import *
from grader.testcase import TestCase
from grader.utils import setDescription, is_function
from functools import wraps

def test_decorator(decorator):
    """ Decorator for test decorators.

        This makes the decorator work testcases decorated with
        :func:`grader.wrappers.test_cases`. """
    @wraps(decorator)
    def _inner(f):
        if isinstance(f, list) or isinstance(f, tuple):
            return tuple(decorator(func) for func in f)
        else:
            return decorator(f)
    return _inner


def test(test_function):
    """ Decorator for a test. The function should take a single argument which
        is the object containing stdin, stdout and module (the globals of users program).

        The function name is used as the test name, which is a description for the test
        that is shown to the user. If the function has a docstring, that is used instead.

        Raising an exception causes the test to fail, the resulting stack trace is
        passed to the user. """
    assert hasattr(test_function, '__call__'), \
        "test_function should be a function, got " + repr(test_function)

    @wraps(test_function)
    def wrapper(module, *args, **kwargs):
        if module.caughtException:
            raise module.caughtException
        result = test_function(module, *args, **kwargs)
        if module.caughtException:
            raise module.caughtException
        return result

    name = get_test_name(test_function)
    if not hasattr(wrapper, "_grader_settings_"):
        wrapper._grader_settings_ = DEFAULT_TEST_SETTINGS.copy()

    testcases[name] = TestCase(name, wrapper, wrapper._grader_settings_)
    return wrapper


@test_decorator
def set_description(d):
    """ Decorator for setting the description of a test.

        Example usage::

            @grader.test
            @grader.set_description("New description")
            def a_test_case(m):
                ...
    """
    def inner(f):
        setDescription(f, d)
        return f
    return inner

def template(template):
    """ Decorator for a test. Indicates how long the test can run. """
    @test_decorator
    def _inner(test_function):
        set_setting(test_function, "template", template)
        return test_function
    return _inner


def timeout(seconds):
    """ Decorator for a test. Indicates how long the test can run. """
    @test_decorator
    def _inner(test_function):
        set_setting(test_function, "timeout", seconds)
        return test_function
    return _inner

def input(args):
    return before_test(create_file('input', args))


def test_cases(test_args, description=None, timelimit=1.0, pattern="${code}", **arg_functions):
    """ Decorator for generating multiple tests with additional arguments.

        :param test_args: Each element of the list is a list of arguments to add to test function call.
        :type test_args: [args...]
        :param str description: String or function, gets passed in keywords and arguments.
        :param double timelimit: Time for execution.
        :keyword function arg_functions: Keyword arguments for the test function.

        :return: list of test functions

        Example usage::

            @test_cases(
                [[1, 2], [3, 4]],
                expected=lambda x, y: x+y,
                description="Adding {0} and {1} should yield {expected}"
            )
            def t(m, a, b, expected):
                # a and b are either 1 and 2 or 3 and 4
                assert a + b == expected

        This is equivelent to::

            @test
            @set_description("Adding 1 and 2 should yield 3")
            def t_1(m):
                assert 1+2 == 3


            @test
            @set_description("Adding 3 and 4 should yield 7")
            def t_2(m):
                assert 3+4 == 7
    """

    if description is None:
        description = ", ".join(str(key)+"=["+value+"]" for key, value in enumerate(test_args))

    def calc_function_kwargs(values):
        out = {}
        for k, fun in arg_functions.items():
            out[k] = fun(*values)
        return out

    def _inner(function):
        # remove from tests if there
        def make_f(args, kw):
            if is_function(description):
                test_desc = description(*args, **kw)
            else:
                test_desc = description.format(*args, **kw)

            @test
            @set_description(test_desc)
            @timeout(timelimit)
            @template(pattern)
            @input(args)
            def _inner(m, *extra_args, **extra_kw):
                _kw = dict(list(kw.items()) + list(extra_kw.items()))
                _args = list(args) + list(extra_args)
                function(m, *_args, **_kw)
            return _inner

        tests = []
        for args in test_args:
            if not isinstance(args, list) and not isinstance(args, tuple):
                args = [args]
            kw = calc_function_kwargs(args)
            tests.append(make_f(args, kw))
        return tests

    return _inner

def before_test(action):
    """ Decorator for a pre-hook on a tested function. Makes the tester execute
        the function `action` before running the decorated test. """
    @test_decorator
    def _inner_decorator(test_function):
        hooks = get_setting(test_function, "pre-hooks") + (action,)
        set_setting(test_function, "pre-hooks", hooks)
        return test_function
    return _inner_decorator


def after_test(action):
    """ Decorator for a post-hook on a tested function. Makes the tester execute
        the function `action` after running the decorated test. """
    @test_decorator
    def _inner_decorator(test_function):
        hooks = get_setting(test_function, "post-hooks") + (action,)
        set_setting(test_function, "post-hooks", hooks)
        return test_function
    return _inner_decorator


def create_file(filename, contents=""):
    """ Hook for creating files before a test.

        Example usage::

            @grader.test
            @grader.before_test(create_file('hello.txt', 'Hello world!'))
            @grader.after_test(delete_file('hello.txt'))
            def hook_test(m):
                with open('hello.txt') as file:
                    txt = file.read()
                    # ...
    """
    import collections
    if isinstance(contents, collections.Iterable) and not isinstance(contents, str):
        contents = "\n".join(map(str, contents))

    def _inner(info):
        with open(filename, "w") as f:
            f.write(contents)

    return _inner


def delete_file(filename):
    import os
    """ Hook for deleting files after a test.

        Example usage::

            @grader.test
            @grader.before_test(create_file('hello.txt', 'Hello world!'))
            @grader.after_test(delete_file('hello.txt'))
            def hook_test(m):
                with open('hello.txt') as file:
                    txt = file.read()
                    # ...
    """

    def _inner(result):
        try:
            os.remove(filename)
        except:
            pass

    return _inner
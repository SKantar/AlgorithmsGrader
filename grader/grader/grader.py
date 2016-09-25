from grader.utils import OrderedDictionary, beautifyDescription
from grader.working_directory import WorkingDirectory
import inspect

testcases = OrderedDictionary()

DEFAULT_TEST_SETTINGS = {
    # hooks that run before tests
    "pre-hooks": (),
    # hooks that run after tests
    "post-hooks": (),
    # timeout for function run
    "timeout": 1.0,
    # check template
    "template": "${code}",
}


def test_submission(language, tester_path, solution_path, other_files=None):
    """ Runs all tests for the solution given as argument.

        :param str language: Language of solution
        :param str tester_path: Path to the tester used.
        :param str solution_path: Path to the solution being tested.
        :param list other_files: Paths to other files to put into same directory while testing.

        :return: Dictionary of test results.

        Return value format::

            {
                "results": [
                    {
                        "description": str, # test description
                        "success": bool, # indicates whether the test case was successful
                        "time": "0.101", # float indicating how long test took
                        "error_message": str, # error message if test was not successful
                        "traceback": str, # full error traceback if test was not successful
                    },
                    ...
                ],
                "success": bool, # indicates whether tests were run or not
                "reason": str, # short string describing why tester failed to run
                "extra_info": dict, # extra information about why tester failed to run
            }
    """

    if not other_files:
        other_files = []

    with WorkingDirectory(language, tester_path, solution_path, other_files) as assets:

        try:
            testcases.load_from(assets.tester_path)
        except Exception as e:
            return _test_load_failure(e)

        if len(testcases) == 0:
            return _fail_result("No tests found in tester")

        test_results = []
        for testname, testcase in testcases.items():
            result = testcase.run(language, assets.tester_path, assets.solution_path)
            test_results.append(result)

    results = {"results": test_results, "success": True}
    return results


def test_code(language, tester_code, user_code, other_files=None):
    """ Tests code. See :func:`test_module` for argument and return value description. """
    if not other_files:
        other_files = []

    with WorkingDirectory(language, tester_code, user_code, other_files, is_code=True) as assets:
        return test_submission(
            language,
            assets.tester_path,
            assets.solution_path,
            assets.other_files
        )


def _fail_result(reason, **extra_info):
    result = {
        "success": False,
        "reason": reason,
        "extra_info": extra_info
    }
    return result


def _test_load_failure(exception):
    from grader import utils
    return _fail_result(
        "Load tests failure",
        error_message=utils.get_error_message(exception),
        traceback=utils.get_traceback(exception))


def get_test_name(function):
    """ Returns the test name as it is used by the grader. Used internally. """
    name = function.__name__
    if inspect.getdoc(function):
        name = beautifyDescription(inspect.getdoc(function))
    return name


def get_setting(test_function, setting_name):
    """ Returns a test setting. Used internally. """
    if isinstance(test_function, str):
        test_function = testcases[test_function]
    if not hasattr(test_function, "_grader_settings_"):
        test_function._grader_settings_ = DEFAULT_TEST_SETTINGS.copy()
    return test_function._grader_settings_[setting_name]


def set_setting(test_function, setting_name, value):
    """ Sets a test setting. Used internally. """
    if isinstance(test_function, str):
        test_function = testcases[test_function]
    get_setting(test_function, setting_name)
    test_function._grader_settings_[setting_name] = value

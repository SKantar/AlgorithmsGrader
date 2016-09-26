from time import time, sleep
from grader.utils import load_json


RESULT_DEFAULTS = {
    "log": [],
    "error_message": "",
    "traceback": ""
}

def call_all(function_list, *args, **kwargs):
    for fun in function_list:
        fun(*args)

class TestCase(object):
    """
        Class represents test case
    """
    def __init__(self, name, function, options):
        self._name = name
        self._function = function
        self._options = options

    def run(self, language, tester_path, solution_path):
        """ Calls the test, checking if it doesn't raise an Exception.
            Returns a dictionary in the following form::

                {

                    "success": boolean,
                    "traceback": string ("" if None)
                    "error_message: string
                    "time": string (execution time, rounded to 3 decimal digits)
                    "description": string (test name/its description)
                }

            If the test timeouts, traceback is set to "timeout".

            Post-hooks can manipulate with the test results before returning.
        """
        from grader.grader import get_setting, testcases
        from grader.terminal import call_test

        test_index = list(testcases.keys()).index(self._name)

        start = time()
        success, stdout, stderr = call_test(test_index,
                                            language,
                                            tester_path,
                                            solution_path,
                                            self._options) # call terminal command
        end = time()

        result = RESULT_DEFAULTS.copy()
        if (end - start) > self._options["timeout"]:
            result["error_message"] = "Timeout"
            result["traceback"] = "Timeout"
        else:
            try:
                result = load_json(stdout)
            except Exception as e:
                result["traceback"] = stdout
                result["stderr"] = stderr

        result.update(
            success=success,
            description=self._name,
            time=("%.3f" % (end - start))
        )

        call_all(self._options["post-hooks"], result)
        return result
from time import sleep
from mako.template import Template
from grader.grader import testcases
from grader.utils import import_module, get_error_message, get_traceback, dump_json, read_code
from grader.program_container import ProgramContainer


RESULT_DEFAULTS = {
    "log": [],
    "error_message": "",
    "traceback": ""
}

def call_all(function_list, *args, **kwargs):
    """ Call all functions from argument list """
    for fun in function_list:
        fun(*args)

def call_test_function(test_index, language, tester_path, solution_path):
    """ Called in another process. Finds the test `test_name`,  calls the
        pre-test hooks and tries to execute it.

        If an exception was raised by call, prints it to stdout """

    import_module(tester_path)                                          # import testcases

    test_name = list(testcases.keys())[test_index]                      # calculate testname of test with index "text_index"
    testcase = testcases[test_name]                                     # get testcase with calculated name

    # pre-test hooks
    pre_hook_info = {                                                   # set arguments for functions we want to call
        "test_name": test_name,                                         # before we run student submission
        "tester_path": tester_path,                                     # ("before_test" functions)
        "solution_path": solution_path,
        "extra_args": [],
        "extra_kwargs": {}
    }
    call_all(testcase._options["pre-hooks"], pre_hook_info)             # call all "before_test" functions

    results = RESULT_DEFAULTS.copy()

    solution_code = read_code(solution_path)                            # read code from students submission

    template = Template(testcase._options["template"])                  # get template from grader

    with open(solution_path, 'w') as f:                                 # render new source code using template
        f.write(template.render(code=solution_code))                    # and make submission executable

    module = None
    # start users program
    try:
        module = ProgramContainer(language, solution_path, results)     # run executable submission
        while not hasattr(module, "module"):
            sleep(0.001)
        module.condition.acquire()
        testcase._function(                                             # when we get results, chek them using key
            module,
            *pre_hook_info["extra_args"],
            **pre_hook_info["extra_kwargs"]
        )
    except Exception as e:                                              # if we got some error, add to result
        if module.caughtException is not None:
            e = module.caughtException
        results["error_message"] = get_error_message(e)
        results["traceback"] = get_traceback(e)
        raise
    finally:
        print(dump_json(results))                                       # return response to stdout
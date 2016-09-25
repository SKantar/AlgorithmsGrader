""" An utility module containing utility functions used by the grader module
    and some useful pre-test hooks.
"""

def import_module(path, name=None):
    if name is None:
        name = path
    import importlib.machinery
    loader = importlib.machinery.SourceFileLoader(name, path)
    module = loader.load_module(name)
    return module

def is_function(value):
    try:
        return hasattr(value, '__call__')
    except:
        return False

## Function descriptions
def beautifyDescription(description):
    """ Converts docstring of a function to a test description
        by removing excess whitespace and joining the answer on one
        line """
    lines = (line.strip() for line in description.split('\n'))
    return " ".join(filter(lambda x: x, lines))


def setDescription(function, description):
    from grader.grader import get_test_name, testcases
    old_description = get_test_name(function)
    if old_description in testcases:
        testcases.remove(old_description)
    description = beautifyDescription(description)
    function.__doc__ = description
    testcases[description] = function


## Json managing
def load_json(json_string):
    " Loads json_string into an dict "
    import json
    return json.loads(json_string)


def dump_json(ordered_dict):
    " Dumps the dict to a string, indented "
    import json
    return json.dumps(ordered_dict, indent=4)


def get_error_message(exception):
    type_ = type(exception)
    return "{}: {}".format(type_.__name__, str(exception))


def get_traceback(exception):
    import traceback
    type_, value, tb = type(exception), exception, exception.__traceback__
    return "".join(traceback.format_exception(type_, value, tb))

def read_code(path):
    import tokenize
    # encoding-safe open
    with tokenize.open(path) as sourceFile:
        contents = sourceFile.read()
    return contents

from collections import OrderedDict
class OrderedDictionary(OrderedDict):
    """ Dictionary for storing testcases """
    def load_from(self, module_path):
        self.clear()
        import_module(module_path)

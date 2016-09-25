from grader import decorators

@decorators.test_cases(
    [[1, 2], [3, 4]],
    expected = lambda x, y: x+y,
    description = "Adding {0} and {1} should yield {expected}",
    timelimit = 300,
)
def check_adding(m, a, b, expected):
    if not isinstance(m.response, int):
        raise Exception("Expected integer but got '%s'" % (type(m.response)))

    if m.response != expected:
        raise Exception("Trazena vrednost %s dobijena %s" % (expected, m.response))

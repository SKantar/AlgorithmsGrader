from grader import decorators
from grader import utils
import ast

template="""${code}
alist = []
n = int(input())
for i in range(n):
    alist.append(int(input()))
print(bubbleSort(alist))
"""


def allowed(code):
    if "sorted" in code:
        return False
    return True

def register_test(description, input, timeline=1, template="${code}"):
    @decorators.test
    @decorators.set_description(description)
    @decorators.input(input)
    @decorators.timeout(timeline)
    @decorators.template(template)

    def check_sort(m):

        if not allowed(utils.read_code(m.module_path)):
            raise Exception("You can not use python function 'sorted'")

        x = m.response
        test = x[0]
        for i in range(len(x)):
            if i == 0:
                continue
            if x[i] < test:
                raise Exception("Ocekivana vrednost '%s', dobijena '%s'" % (str(sorted(x)), str(m.response)))


register_test(
    "Sort next list [54, 26, 93, 17, 77, 31, 44, 55, 20]",
    [9, 54, 26, 93, 17, 77, 31, 44, 55, 20],
    1,
    template
)

register_test(
    "Sort next list [1, 2, 3, 4, 5, 6, 7, 8, 9]",
    [9, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    1,
    template
)

register_test(
    "Sort next list [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]",
    [10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    1,
    template
)

register_test(
    "Sort next list [58, 23]",
    [2, 58, 23],
    1,
    template
)


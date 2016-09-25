Hybrid Algorithms Grader
=============
(Python 3, Python 2, Java, C/C++, C#, PHP)

This is a module for automatically testing homework solutions that has been used for giving feedback for homeworks and midterms for various first-year programming courses.

For the student, feedback provided by the module should be helpful for debugging and understanding where they went wrong.

For the teacher, the advantage over using normal unit tests is that it allows to move from purely-manual based input-output testing to a more structured and consistent framework that saves time.


## Example

###Task statement
Write Python function 'bubbleSort(list)' to sort N numbers in ascending order using Bubble sort

###Tester [grade_function.py](grader/tests/sort_function/grade_function.py)
```python
from grader import decorators
from grader import utils

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
                raise Exception("Ocekivana vrednost '%s', dobijena '%s'" %
                                (str(sorted(x)), str(m.response)))


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
```

###Correct Solution [correct_solution.py](grader/tests/sort_function/correct_solution.py)
```python
def bubbleSort(alist):
    for passnum in range(len(alist)-1,0,-1):
        for i in range(passnum):
            if alist[i]>alist[i+1]:
                temp = alist[i]
                alist[i] = alist[i+1]
                alist[i+1] = temp
    return alist
```
## Setup

**Prerequsite**:<br/>
    - Install [python3.5](https://www.python.org), preferably use a virtualenv.<br/>
    - Install [docker](https://www.docker.com/) for linux<br/>

### Running test on a file
To tester on a solution, run `python __main__.py <language> <tester_file> <solution_file>`.

For example, to run the above tester (in the tests folder) on the sample solution:
```bash
cd grader
python __main__.py python3 tests/sort_function/grade_function.py tests/sort_function/correct_solution.py
```


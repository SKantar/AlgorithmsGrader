import sys, os
import ast
from threading import Thread, Condition
from time import sleep

from grader.terminal import call_command
from grader.config import calculate_compile_and_execute_command

STATUS = 0
RESULT = 1
EXCEPTION = 2

class SyncCondition(Condition):
    def __init__(self):
        self.finished = False
        self.release_count = 0
        Condition.__init__(self)

    def notify_release(self):
        if self.finished: return
        self.release_count += 1
        self.notify()
        self.release()

    def wait_next_release(self):
        if self.finished: return
        target_release_count = self.release_count
        while self.release_count <= target_release_count:
            sleep(0.00001)

    def finish(self):
        # called by program container, to mark that everything is finished
        self.finished = True

class ProgramContainer(Thread):
    """ The thread in which the users program runs """

    def __init__(self, lang, module_path, results):
        Thread.__init__(self)
        self.lang = lang
        self.module_path = module_path
        self._results = results
        self._response = ""
        self.condition = SyncCondition()

        self.caughtException = None
        self.__startProgram()

    def __startProgram(self):
        self.setDaemon(True)
        self.start()
        self._started = False

    def run(self):

        self.condition.acquire()
        self._started = True
        self.finished = False

        try:
            self._exec_code()
        except Exception as error:
            self.caughtException = error

        self.condition.notify_release()
        self.condition.finish()
        self.finished = True

    def _exec_code(self):
        from types import ModuleType
        mod = ModuleType("__main__")
        self.module = mod

        file_path = os.path.dirname(self.module_path)
        file_name = os.path.basename(self.module_path)

        response = call_command(calculate_compile_and_execute_command(self.lang, file_path, file_name, 'input' in os.listdir(file_path)))

        if response[STATUS] == 0:
            if response[RESULT]:
                self._response = ast.literal_eval(response[RESULT].rstrip())
        else:
            raise Exception("%s\n%s" % (response[RESULT], response[EXCEPTION]))

        return mod

    def log(self, what):
        self._results["log"].append(what)

    @property
    def response(self):
        return self._response
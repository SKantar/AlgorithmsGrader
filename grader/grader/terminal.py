import os
import subprocess
import datetime
import signal
import time
import sys

CURRENT_FOLDER = os.path.abspath(os.path.dirname(__file__))
SANDBOX_DIR = os.path.join(CURRENT_FOLDER, "sandbox")

TEST_RUN_CMD = [sys.executable, os.path.join(SANDBOX_DIR, "run_test")]


def read_proc_results(proc, decode):
    stdout = proc.stdout.read()
    stderr = proc.stderr.read()
    if decode:
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
    status = proc.returncode
    return status, stdout, stderr

def microseconds_passed(time_delta):
    return time_delta.microseconds + time_delta.seconds * 10**6


def call_command(cmd, timeout=float('inf'), cwd=None, decode=True, **subproc_options):
    """
        Call sistem command in terminal
    :param cmd: command
    :param timeout: time limit for command execution
    :param cwd: current working directory
    :param decode: decoding
    :param subproc_options: optional params
    :return:
    """
    if cwd is None:
        cwd = os.getcwd()

    start = datetime.datetime.now()

    subproc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **subproc_options
    )
    reached_timeout = False
    while subproc.poll() is None:
        time.sleep(0.02)
        now = datetime.datetime.now()
        if microseconds_passed(now-start) >= timeout * 10**6:
            subproc.kill()
            os.kill(subproc.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            reached_timeout = True
            #break

    status, stdout, stderr = read_proc_results(subproc, decode)
    if reached_timeout:
        status = 1
    return status, stdout, stderr


def call_test(test_index, language, tester_path, solution_path, options):
    """
        Call test case using params
    :param test_index: number of tc
    :param language: language of submission
    :param tester_path: path of key
    :param solution_path: path of submission
    :param options: optional params
    :return:
    """
    from grader.config import SCRIPTS
    # this assumes that tester, solution resides in the same path
    #working_dir = os.getcwd()#os.path.dirname(tester_path)
    cmd = TEST_RUN_CMD + [
        language,
        tester_path,
        solution_path,
        SCRIPTS[language.lower()],
        str(test_index)
    ]
    timeout = options.get('timeout', 1.0)
    status, stdout, stderr = call_command(cmd, timeout)
    return status == 0, stdout, stderr

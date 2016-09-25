import os
import sys
from shutil import copy, rmtree
from tempfile import NamedTemporaryFile, mkdtemp

EXTENSIONS = {
    'java': '.java',
    'c': '.c',
    'c#': '.mono',
    'mono': '.mono',
    'python': '.py',
    'python2': '.py',
    'python3': '.py',
    'php': '.php'
}

class WorkingDirectory(object):
    """
        Class represent current working directory
    """

    def __init__(self, language, tester_path, solution_path, other_files=list(), is_code=False, add_to_path=True):
        self.path = mkdtemp()
        if is_code:
            creator_function = self._write
        else:
            creator_function = self._copy

        self.tester_path = creator_function(tester_path)
        self.solution_path = creator_function(solution_path, language=language)

        self.other_files = list(map(self._copy, other_files))

        for file in self.other_files:
            os.chmod(file, 777)

        self.add_to_path = add_to_path
        if add_to_path:
            sys.path.append(self.path)
            self.original_cwd = os.getcwd()
            os.chdir(self.path)

    def _copy(self, file_path, language=None):
        """
            Copy file from location
        :param file_path: file location
        :param language: language of file
        :return: file path
        """
        # returns path
        if os.path.isdir(file_path):
            files = os.listdir(file_path)
            return [self._copy(os.path.join(file_path, name)) for name in files]
        return copy(file_path, self.path)

    def _write(self, code, language='python'):
        """
            Write code written in language "language"
        :param code: source code
        :param language: language of source code
        :return: path
        """
        file = NamedTemporaryFile(
            dir=self.path,
            mode="w",
            suffix=EXTENSIONS[language],
            delete=False
        )
        file.write(code)
        file.close()
        return file.name

    def remove(self):
        if self.add_to_path:
            sys.path.remove(self.path)
            os.chdir(self.original_cwd)
        if not os.path.exists(self.path):
            raise IOError("{} already doesn't exist".format(self.path))
        rmtree(self.path)

    def files_in_path(self):
        return os.listdir(self.path)

    def __enter__(self): 
        return self

    def __exit__(self, *args):
        self.remove()

    def __str__(self):
        return "<Assets: %s %s %s>" % (self.tester_path, self.solution_path, self.other_files)

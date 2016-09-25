LANGUAGES = ["java", "c", "c#", "mono", "python", "python2", "python3", "php"]

SCRIPTS = {
    "java": "compile_and_run_java",
    "c": "compile_and_run_c",
    "c#": "compile_and_run_mono",
    "mono": "compile_and_run_mono",
    "python": "run_python2",
    "python2": "run_python2",
    "python3": "run_python3",
    "php": "run_php"
}

BASE_CMD = [
    "docker",
    "run",
    "--rm",
    "-v"
]


def calculate_compile_and_execute_command(lang, folder_name, file_name, input=False):
    """
        Calculate terminal command for params
    :param lang: language from LANGUAGES list, language of submission
    :param folder_name: directory of submission file
    :param file_name: submission filename
    :param input: user stdio
    :return: list of single params for linux command
    """

    if lang.lower() == "c":
        return calculate_compile_and_execute_c_command(folder_name, file_name, input)
    elif lang.lower() == "java":
        return calculate_compile_and_execute_java_command(folder_name, file_name, input)
    elif lang.lower() == "c#" or lang.lower() == "mono":
        return calculate_compile_and_execute_cs_command(folder_name, file_name, input)
    elif lang.lower() == "python2":
        return calculate_compile_and_execute_python2_command(folder_name, file_name, input)
    elif lang.lower() == "python3" or lang.lower() == "python":
        return calculate_compile_and_execute_python3_command(folder_name, file_name, input)
    elif lang.lower() == "php":
        return calculate_compile_and_execute_php_command(folder_name, file_name, input)


def calculate_compile_and_execute_c_command(folder_name, file_name, input):
    """
        Calculate comand for C programs
    :param folder_name: directory of submission file
    :param file_name: submission filename
    :param input: user stdio
    :return: list of single params for linux command
    """
    command = BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "skantar/linux-gcc",
        "./compile_and_run_c",
        file_name
    ]

    if input:
        command.append("input")
    return command


def calculate_compile_and_execute_java_command(folder_name, file_name, input):
    """
        Calculate comand for Java programs
    :param folder_name: directory of submission file
    :param file_name: submission filename
    :param input: user stdio
    :return: list of single params for linux command
    """
    command = BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "skantar/linux-java8",
        "./compile_and_run_java",
        file_name
    ]

    if input:
        command.append("input")
    return command



def calculate_compile_and_execute_cs_command(folder_name, file_name, input):
    """
        Calculate comand for C# programs
    :param folder_name: directory of submission file
    :param file_name: submission filename
    :param input: user stdio
    :return: list of single params for linux command
    """
    command = BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "skantar/linux-csharp",
        "./compile_and_run_mono",
        file_name
    ]

    if input:
        command.append("input")
    return command



def calculate_compile_and_execute_python2_command(folder_name, file_name, input):
    """
        Calculate comand for Python2 programs
    :param folder_name: directory of submission file
    :param file_name: submission filename
    :param input: user stdio
    :return: list of single params for linux command
    """
    command = BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "skantar/linux-python2",
        "./run_python2",
        file_name
    ]
    
    if input:
        command.append("input")
    return command



def calculate_compile_and_execute_python3_command(folder_name, file_name, input):
    """
        Calculate comand for Python3 programs
    :param folder_name: directory of submission file
    :param file_name: submission filename
    :param input: user stdio
    :return: list of single params for linux command
    """
    command = BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "skantar/linux-python3",
        "./run_python3",
        file_name
    ]

    if input:
        command.append("input")
    return command



def calculate_compile_and_execute_php_command(folder_name, file_name, input):
    """
        Calculate comand for PHP programs
    :param folder_name: directory of submission file
    :param file_name: submission filename
    :param input: user stdio
    :return: list of single params for linux command
    """
    command = BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "skantar/linux-php",
        "./run_php",
        file_name
    ]

    if input:
        command.append("input")
    return command


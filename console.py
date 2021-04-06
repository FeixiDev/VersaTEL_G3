import sys


class ExitCode(object):
    OK = 0
    UNKNOWN_ERROR = 1
    ARGPARSE_ERROR = 2
    OBJECT_NOT_FOUND = 3
    OPTION_NOT_SUPPORTED = 4
    ILLEGAL_STATE = 5
    CONDITION_NOT_SUPPORTED = 6
    CONNECTION_ERROR = 20
    CONNECTION_TIMEOUT = 21
    UNEXPECTED_REPLY = 22
    API_ERROR = 10
    NO_SATELLITE_CONNECTION = 11

class Console():
    def __init__(self, stdin=sys.stdin, stdout=sys.stdout):
        self._stdout = stdout
        self._stdin = stdin


    # 之后可附加日志的记录
    def normal_output(self,text):
        self._stdout.write(text,'\n')
        self._stdout.flush()


    def error_output(self,text,exit_code):
        self._stdout.write(text,'\n')
        sys.exit(exit_code)


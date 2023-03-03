import sys
from typing import Any, Text, NoReturn

import rasa.shared.utils.io


def print_blocking(message) -> None:
    """Save fcntl settings and restore them after print().

    Args:
        message: The message to be printed.
    """
    try:
        # this code block is intended to work around a BlockingIOError seen
        # intermittently under mysterious circumstances, by the light of a
        # full moon
        from fcntl import fcntl, F_GETFL, F_SETFL
        from os import O_NONBLOCK 
        save = fcntl(sys.stdout.fileno(), F_GETFL)
        new = save & ~O_NONBLOCK
        fcntl(sys.stdout.fileno(), F_SETFL, new)
        print(message)
        fcntl(sys.stdout.fileno(), F_SETFL, save)
        sys.stdout.flush()
    except ImportError:
        print(message)

def print_color(*args: Any, color: Text) -> None:
    """Print the given arguments to STDOUT in the specified color.

    Args:
        args: A list of objects to be printed.
        color: A textual representation of the color.
    """
    output = rasa.shared.utils.io.wrap_with_color(*args, color=color)
    try:
        # colorama is used to fix a regression where colors can not be printed on
        # windows. https://github.com/RasaHQ/rasa/issues/7053
        from colorama import AnsiToWin32

        stream = AnsiToWin32(sys.stdout).stream
        print(output, file=stream)
    except ImportError:
        try:
            print(output)
        except BlockingIOError:
            print_blocking(output)


def print_success(*args: Any) -> None:
    """Print the given arguments to STDOUT in green, indicating success.

    Args:
        args: A list of objects to be printed.
    """
    print_color(*args, color=rasa.shared.utils.io.bcolors.OKGREEN)


def print_info(*args: Any) -> None:
    """Print the given arguments to STDOUT in blue.

    Args:
        args: A list of objects to be printed.
    """
    print_color(*args, color=rasa.shared.utils.io.bcolors.OKBLUE)


def print_warning(*args: Any) -> None:
    """Print the given arguments to STDOUT in a color indicating a warning.

    Args:
        args: A list of objects to be printed.
    """
    print_color(*args, color=rasa.shared.utils.io.bcolors.WARNING)


def print_error(*args: Any) -> None:
    """Print the given arguments to STDOUT in a color indicating an error.

    Args:
        args: A list of objects to be printed.
    """
    print_color(*args, color=rasa.shared.utils.io.bcolors.FAIL)


def print_error_and_exit(message: Text, exit_code: int = 1) -> NoReturn:
    """Print an error message and exit the application.

    Args:
        message: The error message to be printed.
        exit_code: The program exit code, defaults to 1.
    """
    print_error(message)
    sys.exit(exit_code)

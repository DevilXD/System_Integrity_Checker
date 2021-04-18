import os
import sys
import subprocess
from time import sleep
from typing import Optional, Callable, TypeVar, cast

# Platform-dependent imports
try:
    import msvcrt
except (ModuleNotFoundError, ImportError):
    # This can happen on non-Windows systems, in which case the check in main.py will exit
    # the program early, before msvcrt gets to be used, which should prevent an error about it
    # being undefined from popping up.
    pass


_RV = TypeVar("_RV")


def get_console_encoding() -> str:
    # Find out the console encoding
    return cast(str, os.device_encoding(1))  # '1' is the stdout on windows


def clear_console():
    subprocess.run("cls")


def get_key(
    prompt: str,
    check: Callable[[str], Optional[_RV]],
    *,
    confirmation: bool = True,
    print_key: bool = True,
) -> _RV:
    """
    Request a key to be pressed by the user. Usually used to choose an option.

    Parameters
    ----------
    prompt : str
        The prompt displayed for this request.
    check : Callable[[str], Optional[_RV]]
        A callable that should aceept the pressed key, and return a value of choosing.
        That value will then be used as the return value of the get_key function.
        If the key was incorrect, returning `None` will ask for user input again.
    confirmation : bool
        Controls if pressing Enter is required to proceed with the picked option.\n
        Defaults to `True`.\n
        Setting this to `False` will proceed with the check, right after pressing
        the selected key, without needing to press Enter.
    print_key : bool
        Controls if the key itself should be printed after pressing it.
        Applies only if `confirmation` is set to `False` - with confirmation enabled,
        the pressed keys are always displayed, and this option is ignored.

    Returns
    -------
    _RV
        Whatever was returned from the check function, for the key given.
    """
    while True:
        key: str
        if confirmation:
            key = input(prompt)
        else:
            print(prompt, end='')
            key = msvcrt.getch().decode()
            if print_key:
                print(key, end='')
        result: Optional[_RV] = check(key)
        if result is not None:
            return result


def ask_restart():
    option = get_key(
        "A restart is required. Do you want to restart now? (Y/N) ",
        lambda c: c in ("Y", "y", "N", "n") and c or None
    )
    if option.lower() == "y":
        print("Restarting...")
        subprocess.run("shutdown /r /t 0", capture_output=True)
        sleep(3)
        sys.exit(0)

import os
import sys
import subprocess
from time import sleep
from typing import Optional, Callable, TypeVar, cast

# Platform-dependent imports
try:
    import msvcrt
except (ModuleNotFoundError, ImportError):
    pass


_RV = TypeVar("_RV", str, int)


def get_console_encoding() -> str:
    # Find out the console encoding
    return cast(str, os.device_encoding(1))  # '1' is the stdout on windows


def clear_console():
    subprocess.run("cls")


def get_key(check: Callable[[str], Optional[_RV]], *, print_keys: bool = False) -> _RV:
    while True:
        key: str = msvcrt.getch().decode()  # type: ignore
        if print_keys:
            print(key, end='')
        result: Optional[_RV] = check(key)
        if result is not None:
            return result


def ask_restart():
    print("A restart is required. Do you want to restart now? (Y/N) ")
    option = get_key(lambda c: c in ("Y", "y", "N", "n") and c or None)
    if option.lower() == "y":
        print("Restarting...")
        subprocess.run("shutdown /r /t 0", capture_output=True)
        sleep(3)
        sys.exit(0)

import os
import re
import subprocess
from functools import partial
from typing import List, NewType, cast

from utils import get_console_encoding


console_encoding = get_console_encoding()


Drive = NewType("Drive", str)


# Get a list of logical drive letters
def get_logical_drives() -> List[Drive]:
    result = subprocess.run("wmic logicaldisk where drivetype=3 get caption", capture_output=True)
    # Example stdout: b'Caption  \r\r\nC:       \r\r\nD:       \r\r\nE:       \r\r\n\r\r\n'
    return cast(List[Drive], [
        l[:2]  # only the first two characters of each line (ex: 'C:')
        for l in (
            result.stdout  # output of the command, as a bytes object
            .decode()  # turned into a string
            .split('\n')  # split into a list of lines
            [1:-2]  # skip the first line with "Caption", and last two empty lines
        )
    ])  # Example output: ['C:', 'D:', 'E:']


# Find out the drive where the system is installed on
def get_system_drive() -> Drive:
    return cast(Drive, os.getenv("systemdrive", "C:"))  # Example output: 'C:'


def schedule_check(drive: Drive):
    subprocess.run(f"fsutil dirty set {drive}", capture_output=True)


# Declare a special wrapper function for chkdsk, that can automatically answer with No
# if the disk couldn't be locked. Return value is the error code it returned.
def run_chkdsk(drive: Drive, options: str = '') -> int:
    command = f"chkdsk {drive}"
    if options:
        command += f" {options}"
    process = subprocess.Popen(
        command,
        bufsize=0,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    process.stdin.write(b"\n")
    key = None
    line_array = []
    read = partial(process.stdout.read, 1)
    for byte in iter(read, b''):
        line_array.append(byte)
        if byte == b'\r':
            # read one more to see if '\n' follows
            following = read()
            if following == b'\n':
                line_array.append(following)
            # we have a whole line
            line = b''.join(line_array).decode(console_encoding)
            if following != b'\n':
                # if it wasn't a new line, then we just put it back for the next line
                line_array = [following]
            else:
                line_array = []
            print(line, end='')
            match = re.search(r"\(./(.)\)", line)
            if match:
                key = match[1]
                break
    if key is not None:
        print(key)
        # deny check on the next restart
        process.communicate(input=f"{key}\n".encode(console_encoding), timeout=1)
    else:
        # completed successfully
        process.communicate(timeout=1)
    process.wait()  # wait until the process terminates
    print()  # insert additional newline
    return process.returncode


def run_sfc():
    subprocess.run("sfc /scannow")

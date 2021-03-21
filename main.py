import os
import sys
# import argparse  # TODO: Add an arg interface to this
import traceback
from time import sleep

from utils import ask_restart
from menu import MenuOption, menu
from drive import get_system_drive, get_logical_drives, run_chkdsk, schedule_check, run_sfc

# Platform-dependent imports
try:
    import ctypes
except (ModuleNotFoundError, ImportError):
    pass


# Determine if we need to pause after messages or not
# Useful only for command-line usage
pause = not bool(len(sys.argv) > 1 and sys.argv[1].lower() == "--no-prompt")

try:
    if sys.platform != "win32":
        print("Only Windows supported!\n")
        if pause:
            os.system("pause")
        sys.exit(2)  # unsupported OS
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Administrator privilages required!\n")
        if pause:
            os.system("pause")
        sys.exit(3)  # unsufficient privileges

    # Nice console title
    ctypes.windll.kernel32.SetConsoleTitleW("System Integrity Verificator (by DevilXD)")
    system_drive = get_system_drive()
    logical_drives = get_logical_drives()

    # Define all possible menu options

    def check_other_drives():
        errors_fixed = False
        restart_required = False
        # Run 'chkdsk' on each drive that isn't the 'system_drive'
        for drive_letter in logical_drives:
            if drive_letter == system_drive:
                continue  # skip this one for now
            print(f"Checking {drive_letter}...\n")

            return_code = run_chkdsk(drive_letter, "/f /x")  # output is shown to the user
            if return_code == 1:
                errors_fixed = True
            elif return_code == 3:
                # quietly schedule a check on the next restart
                schedule_check(drive_letter)
                restart_required = True
        return (errors_fixed, restart_required)

    def disk_standard():
        # Check all other drives first
        errors_fixed, _ = check_other_drives()
        # quietly schedule a system drive check on the next restart
        schedule_check(system_drive)
        return (errors_fixed, True)

    def disk_lazy():
        # Check all other drives first
        errors_fixed, restart_required = check_other_drives()
        # Run 'chkdsk' on the 'system_drive' in read-only mode.
        # Schedule a check on the next restart if any problems were found.
        print(f"Checking {system_drive} (system drive)...\n")
        return_code = run_chkdsk(system_drive)
        if return_code > 0:
            # errors found - quietly schedule a check on the next restart
            schedule_check(system_drive)
            restart_required = True
        return (errors_fixed, restart_required)

    # Safe option - schedule a check on all drives on the next restart
    def disk_offline():
        for drive_letter in logical_drives:
            print(f"Scheduling {drive_letter} check...")
            schedule_check(drive_letter)
        print("\nAll disks have been scheduled for a check on the next restart.\n")
        return (False, True)

    # Verifies system files
    def sfc_check():
        run_sfc()
        return (False, False)

    def exit():
        # ¯\_(ツ)_/¯
        print("Goodbye!")
        sleep(1.5)
        sys.exit(0)

    # Menu
    if pause:
        errors_fixed, restart_required = menu(
            "System Integrity Verificator (by DevilXD)\n"
            "\n"
            f"Detected logical drives: {', '.join(logical_drives)}\n"
            f"System drive: {system_drive}",
            [
                MenuOption(
                    "Standard - Lock and check each drive, restart for the system drive check",
                    disk_standard,
                ),
                MenuOption(
                    "Lazy - Lock and check each drive, avoid restarts if possible",
                    disk_lazy,
                ),
                MenuOption(
                    "Offline - Schedule all disks to be checked on the next restart",
                    disk_offline,
                ),
                MenuOption(
                    "Sfc check - verify system files integrity (only after disk checking)",
                    sfc_check,
                ),
                MenuOption("Exit", exit),
            ],
        )
    else:
        # If we're not pausing, just run the standard check
        errors_fixed, restart_required = disk_standard()

    msg = "\nSystem integrity verification completed!"
    if errors_fixed:
        msg += " Integrity has been restored."
    print(f"{msg}\n")
    if restart_required:
        ask_restart()
    elif pause:
        os.system("pause")

    # Exit cleanly
    sys.exit(0)
except KeyboardInterrupt:
    print("\n\nOperation aborted by the user.\n")
    if pause:
        os.system("pause")
    sys.exit(1)
except Exception:
    print()
    traceback.print_exc()
    print()
    if pause:
        os.system("pause")
    sys.exit(1)  # unknown error

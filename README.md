# System_Integrity_Checker
A simple console application, that ensures the integrity of the system files on disk. For Windows only.

### Standard usage instructional:
• Download the latest release and run it as administrator
• Choose one of the 1-3 options (1st recommended)
• Wait for it to complete
• Restart your PC if prompted
• Run the utility again
• Choose the 4th option (SFC check)
• Wait for it to complete
• Restart your PC if prompted (might not prompt you if everything was intact)

### Manual instructions (for advanced users):
• Make sure all non-important applications are closed, and all your important work saved
• Make sure Paladins is closed too
• Open up `cmd` as administrator
• Assuming the `C:` partition is where you have your system installed, run `chkdsk C: /f`. Substitute `C:` for any other partition letter, if your system would be installed elsewhere. The command might prompt you for a check on the next computer restart, shortly after running it. If that would happen, **agree** to it, then restart your PC. __Make sure to not press any buttons during boot up to not skip the check.__
• Find out on which partition you have Paladins installed on. Usually it's either the same as system partition (`C:`), or something like a data partition (`D:`, `E:`, etc.). __If this partition is the same as the system partition, you can skip this step entirely.__ Otherwise, run `chkdsk _: /f /x`, where `_` is the partition letter of where you have Paladins installed on. (example: `chkdsk D: /f /x`, for an installation on `D:`). Wait for it to complete - this one should continue without prompting for restart. If you'd be unsure which partition you have Paladins installed on, it's safe to run this command on every partition you'd have in the system.
• After all partition checking has completed, restart your PC
• Once the computer reboots, open up cmd as administrator again - run `sfc /scannow`. This will verify the integrity of all important system files, and restore those that might've been removed as corrupted during the previous check. Restart your PC if prompted (usually not necessary if all files have been verified successfully, if not, it'll prompt you for restart itself).

### Manual build instructions (for advanced users):
• Install Python 3.8+ (may work on lower versions too)
• Run `pip install -r requirements.txt`
• Run `build.bat` - the built exe can be found in the `/dist` folder

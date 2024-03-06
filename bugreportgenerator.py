"""
This file generates the bugreport from the connected android device.
"""
import glob
import os
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

from rich.progress import Progress

from utilities import checkAdbDevices, displayError


def runSubProcess(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True, )

    while True:
        return_code = process.poll()
        if return_code is not None:
            # Process has completed
            break
        time.sleep(1)
    process.wait()
    stdout, stderr = process.communicate()
    return stdout, process.returncode


class Bugreport:
    TOTAL_PROGRESS = 180

    @classmethod
    def moveBugreport(cls) -> None:
        """
        Moves the existed bugreport in the home dir into "bug reports" folder.
        :return: None
        """
        home_dir = os.path.expanduser('~')
        bugreport_dir = home_dir + "/bug reports"
        file_pattern = os.path.join(home_dir, 'bugreport*.zip')
        os.makedirs(bugreport_dir, exist_ok=True)
        files = glob.glob(file_pattern)
        for file in files:
            if file:
                print(f'Found an existing Bugreport "{file.strip(home_dir)}" in {home_dir}\n')
                shutil.move(file, bugreport_dir)
                print(f'Moved "{file.strip(home_dir)}" to >> {bugreport_dir}\n')

    @classmethod
    def captureBugReport(cls) -> None:
        """
        Captures the Bugreport from the connected Android device.
        :return: None
        """
        # Check for ADB and connected devices
        checkAdbDevices()

        # Move the bugreport
        cls.moveBugreport()

        # Home directory path
        home_dir = os.path.expanduser('~')
        # Set up the ADB command
        adb_command = f"adb bugreport {home_dir}"

        with Progress(transient=True) as progress:
            task = progress.add_task(f"[magenta]Capturing Bug Report...to >> {home_dir} ", total=cls.TOTAL_PROGRESS)
            try:
                with ThreadPoolExecutor() as executor:
                    # Submit the subprocess task to the executor
                    future = executor.submit(runSubProcess, adb_command)

                    # Main thread updates the progress bar
                    while not future.done():
                        time.sleep(1)
                        progress.update(task, advance=1)
                    # Ensure the progress bar reaches completion
                    progress.update(task, completed=cls.TOTAL_PROGRESS)

                    # Retrieve the result from the future
                    stdout, return_code = future.result()

                    if return_code == 0:
                        # Introduce a delay before printing the completion message
                        time.sleep(1)
                        print("\nSUCCESS 🚀 : Bug Report captured.")
                    else:
                        print(f'\nERROR ❗ : Failed to collect the Bugreport.\n{stdout}')

            except Exception as e:
                displayError(f'An unexpected error occurred: {e}')
            except KeyboardInterrupt:
                print('\nINTERRUPT ❗ : Dude.... You interrupted me.. 😬')


if __name__ == "__main__":
    Bugreport.moveBugreport()
    Bugreport.captureBugReport()

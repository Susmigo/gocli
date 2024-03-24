"""
This file all the methods that are required to run the subprocess and ADB commands.
"""
import subprocess

from utils.display import Display
from utils.checks import Checks


class Commands:
    """
    Subprocess commands for running adb commands.
    """

    def __init__(self):
        self.check = Checks()
        self.display = Display()

    def adbCommand(self, _cmd: str) -> str:
        """
        Runs the adb commands using subprocess
        :param _cmd:  adb command in string format
        :return: Output of the command as string
        """
        try:
            if self.check.checkAdbDevices():
                result_ = subprocess.run(_cmd, shell=True, check=True, capture_output=True, text=True)
                return result_.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.display.error_Exit(f"Error executing the command", trace=str(e))
        except KeyboardInterrupt:
            self.display.error_Exit("Interrupted by User.")

    def runSubprocess(self, _cmd: str, timeout=None) -> tuple[int, str]:

        result_ = None
        try:
            result_ = subprocess.run(_cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            if result_.returncode == 0:
                return result_.returncode, result_.stdout.strip()
            else:
                return result_.returncode, result_.stderr.strip()
        except subprocess.CalledProcessError as e:
            return result_.returncode, str(e)
        except KeyboardInterrupt:
            self.display.error_Exit("Interrupted by User.")

    def runSubprocessPopen(self, _cmd: str) -> subprocess:
        """
        Execute a command using subprocess.Popen and capture its output.

        :param: _cmd - The command to be executed.

        :returns: tuple[int, str] - A tuple containing the return code and the command output (stdout or stderr).
        """
        try:
            process = subprocess.Popen(_cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            return_code = process.returncode

            if return_code == 0:
                return return_code, stdout.strip().decode('utf-8')
            else:
                return return_code, stderr.strip().decode('utf-8')
        except subprocess.SubprocessError as e:
            return -1, str(e)
        except KeyboardInterrupt:
            self.display.error_Exit("Interrupted by user")


if __name__ == "__main__":
    cmd = Commands()
    print(cmd.adbCommand('adb devices'))
    output = cmd.runSubprocess('ls -l')
    print("result:", output[0])
    print("output:", output[1])
    output = cmd.runSubprocessPopen('ls -l')
    print("result:", output[0])
    print("output:", output[1])

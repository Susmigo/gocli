import subprocess

from utils.display import Display


class Checks:

    def __init__(self):
        self.display = Display()

    def _runSubprocessPopen(self, _cmd: str) -> tuple[int, str]:
        """
        Execute a command using subprocess.Popen and capture its output.

        :param _cmd: The command to be executed.
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
        except Exception as e:
            return -1, str(e)
        except KeyboardInterrupt:
            self.display.error_Exit("Interrupted by user")

    def checkAdbDevices(self) -> bool:
        """
        Check for ADB installation and whether any device is connected to the laptop.
        :return: bool
        """
        # Check if ADB is installed
        try:
            subprocess.run(["adb", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            self.display.error_Exit("ADB is not installed or not in the system PATH.", trace=str(e))

        # Check for connected devices
        devices_result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True)
        # Extract the list of devices
        device_lines = devices_result.stdout.strip().split('\n')[1:]

        if not any('device' in line for line in device_lines):
            self.display.error_Exit("No Device is connected. Connect a device 📲")
        else:
            return True

    def checkBinary(self, binary: str) -> bool:
        """
        Check whether the user given binary is installed or not in the device.
        :param binary: binary to be checked.

        :return: bool
        """
        try:
            code, output = self._runSubprocessPopen(f"command -V {binary}")
            if code == 0:
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            self.display.error(f"Failed to check the binary {binary} existence", trace=str(e))

    def is_device_connected(self) -> bool:
        """
        checks for the device connected to laptop.

        :return: bool
        """
        try:
            adb_command = ["adb", "devices"]
            result = subprocess.run(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout.strip()
            devices = output.splitlines()[1:]
            if not any('device' in line for line in devices):
                return False
            else:
                return True
        except Exception as e:
            self.display.error_Exit(f"An error occurred while checking device connection: {e}")


if __name__ == "__main__":
    chk = Checks()
    # print(chk.checkAdbDevices())
    # print(chk.checkBinary('gocli'))
    print(chk.is_device_connected())

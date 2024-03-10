"""
This script manages the device details of the connected device.
"""
from utilities import Checks, Errors, Commands


class DeviceDetails:
    def __init__(self):
        self.cmd = Commands()
        self.chk = Checks()
        self.err = Errors()

    def getDeviceInfo(self, prop: str) -> str:
        return self.cmd.runCommand(f'adb shell getprop {prop}')

    def getDeviceManufacturer(self) -> str:
        return self.getDeviceInfo('ro.product.manufacturer')

    def getDeviceModel(self) -> str:
        return self.getDeviceInfo('ro.product.model')

    def getDeviceName(self) -> str:
        return self.getDeviceInfo('ro.product.name')

    def getDeviceBuild(self) -> str:
        return self.getDeviceInfo('ro.build.description')

    def getExperience(self) -> bool:
        return "launcherx" in self.cmd.runCommand('adb shell pm list packages')

    def getLocale(self) -> str:
        return self.getDeviceInfo('persist.sys.locale')

    def finalPrint(self) -> str:
        output = ""
        output += (f"Device: [{self.getDeviceManufacturer()}] {self.getDeviceModel()} "
                   f"({self.getDeviceName()})\n")
        output += f"Build: {self.getDeviceBuild()}"
        return output

    def finalPrintTabulate(self) -> list:
        # Split the string into lines
        lines = self.finalPrint().split('\n')
        # Create the result list using a list comprehension
        result = [["**" + key.strip() + "**", value.strip()] for key, value in
                  (line.split(': ', 1) for line in lines if line)]
        return result


if __name__ == "__main__":
    print("For string:\n", DeviceDetails().finalPrint())
    print("For tabulate:\n", DeviceDetails().finalPrintTabulate())

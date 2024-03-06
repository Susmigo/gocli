"""
This script manages the device details of the connected device.
"""
from utilities import runCommand


class DeviceDetails:
    @classmethod
    def getDeviceInfo(cls, prop: str) -> str:
        return runCommand(f'adb shell getprop {prop}')

    @classmethod
    def getDeviceManufacturer(cls) -> str:
        return cls.getDeviceInfo('ro.product.manufacturer')

    @classmethod
    def getDeviceModel(cls) -> str:
        return cls.getDeviceInfo('ro.product.model')

    @classmethod
    def getDeviceName(cls) -> str:
        return cls.getDeviceInfo('ro.product.name')

    @classmethod
    def getDeviceBuild(cls) -> str:
        return cls.getDeviceInfo('ro.build.description')

    @classmethod
    def getExperience(cls) -> bool:
        return "launcherx" in runCommand('adb shell pm list packages')

    @classmethod
    def getLocale(cls) -> str:
        return cls.getDeviceInfo('persist.sys.locale')

    @classmethod
    def finalPrint(cls) -> str:
        output = ""
        output += (f"Device: [{cls.getDeviceManufacturer()}] {cls.getDeviceModel()} "
                   f"({cls.getDeviceName()})\n")
        output += f"Build: {cls.getDeviceBuild()}"
        return output

    @classmethod
    def finalPrintTabulate(cls) -> list:
        # Split the string into lines
        lines = cls.finalPrint().split('\n')
        # Create the result list using a list comprehension
        result = [["**" + key.strip() + "**", value.strip()] for key, value in
                  (line.split(': ', 1) for line in lines if line)]
        return result


if __name__ == "__main__":
    print("For string:\n", DeviceDetails.finalPrint())
    print("For tabulate:\n", DeviceDetails.finalPrintTabulate())

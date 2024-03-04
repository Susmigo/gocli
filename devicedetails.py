"""
This script manages the device details of the connected device.
"""
from utilities import _run_command


class DeviceDetails:
    @staticmethod
    def get_device_info(prop: str) -> str:
        return _run_command(f'adb shell getprop {prop}')

    @classmethod
    def get_device_manufacturer(cls) -> str:
        return cls.get_device_info('ro.product.manufacturer')

    @classmethod
    def get_device_model(cls) -> str:
        return cls.get_device_info('ro.product.model')

    @classmethod
    def get_device_name(cls) -> str:
        return cls.get_device_info('ro.product.name')

    @classmethod
    def get_device_build(cls) -> str:
        return cls.get_device_info('ro.build.description')

    @classmethod
    def get_experience(cls) -> bool:
        return "launcherx" in _run_command('adb shell pm list packages')

    @classmethod
    def final_print_str(cls) -> str:
        output = ""
        output += (f"Device: [{cls.get_device_manufacturer()}] {cls.get_device_model()} "
                   f"({cls.get_device_name()})\n")
        output += f"Build: {cls.get_device_build()}"
        return output

    @classmethod
    def final_print_for_tabulate(cls) -> list:
        # Split the string into lines
        lines = cls.final_print_str().split('\n')
        # Create the result list using a list comprehension
        result = [["**" + key.strip() + "**", value.strip()] for key, value in
                  (line.split(': ', 1) for line in lines if line)]
        return result


if __name__ == "__main__":
    print("For string:\n", DeviceDetails.final_print_str())
    print("For tabulate:\n", DeviceDetails.final_print_for_tabulate())

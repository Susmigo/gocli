import os
import subprocess
import threading
import time
from datetime import datetime
from threading import Thread

stop_recording = threading.Event()


def is_device_connected():
    try:
        adb_command = ["adb", "devices"]
        result = subprocess.run(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout.strip()
        devices = output.splitlines()[1:]
        for device in devices:
            if "device" in device:
                return True
        return False
    except Exception as e:
        print(f"An error occurred while checking device connection: {e}")
        return False


def get_file_name(starts_with: str, extension: str, file_name: str = None) -> str:
    if file_name is None:
        file_name = starts_with + "_" + datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    return f"{file_name.replace(' ', '_')}.{extension}"


def _start_recording(file_name: str, duration: int = 10):
    _file_name = get_file_name(starts_with='scr', extension='mp4', file_name=file_name)
    _file_path_in_device = f"/sdcard/{_file_name}"
    _file_path_in_laptop = os.path.join(os.path.expanduser('~'))

    recording_process = None
    try:
        _record_command = f"adb shell screenrecord --bugreport --time-limit {duration} {_file_path_in_device}"
        recording_process = subprocess.Popen(_record_command, shell=True)

        while not stop_recording.is_set() and recording_process.poll() is None:
            if not is_device_connected():
                raise subprocess.SubprocessError("Device disconnected")
            time.sleep(1)  # Adjust sleep duration as needed

        if stop_recording.is_set():
            recording_process.terminate()
            recording_process.wait()

        if (recording_process.returncode != 0 and
                recording_process.returncode != -15 and recording_process.returncode != -2):
            raise subprocess.SubprocessError(
                f"Recording process returned non-zero exit status: {recording_process.returncode}")

    except KeyboardInterrupt:
        recording_process.terminate()
    except subprocess.SubprocessError as e:
        print("failed to capture the recording", e)

    _pull_command = f"adb pull {_file_path_in_device} {_file_path_in_laptop}"
    try:
        time.sleep(2)
        _result = subprocess.run(_pull_command, shell=True, check=True, stdout=subprocess.DEVNULL)
        if _result.returncode == 0:
            print("Screen recording pulled successfully.")
        else:
            raise subprocess.CalledProcessError
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to pull screen recording: {e}")


def __stop_recording():
    stop_recording.set()


def screenrecord(name: str = None):
    recording_process = None
    try:
        if is_device_connected():
            recording_process = Thread(target=_start_recording, args=(name,))
            recording_process.start()
            while recording_process.is_alive():
                input("press Enter to terminate the process..")
                break
            __stop_recording()
            recording_process.join()
        else:
            print('Connect a device..')  # TODO: raise no device error.
    except KeyboardInterrupt:
        __stop_recording()
        recording_process.join()


screenrecord()

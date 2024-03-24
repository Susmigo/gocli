import os
import subprocess
import threading
import time
from datetime import datetime

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

def start_recording(file_name: str, duration: int = 10):
    file_name = get_file_name(starts_with='scr', extension='mp4', file_name=file_name)
    file_path_in_device = f"/sdcard/{file_name}"
    file_path_in_laptop = os.path.join(os.path.expanduser('~'))

    recording_process = None
    try:
        record_command = f"adb shell screenrecord --bugreport --time-limit {duration} {file_path_in_device}"
        recording_process = subprocess.Popen(record_command, shell=True)

        while not stop_recording.is_set() and recording_process.poll() is None:
            if not is_device_connected():
                raise subprocess.SubprocessError("Device disconnected")
            time.sleep(1)

        if stop_recording.is_set():
            recording_process.terminate()
            recording_process.wait()

        if recording_process.returncode != 0 and recording_process.returncode != -15:
            raise subprocess.SubprocessError(
                f"Recording process returned non-zero exit status: {recording_process.returncode}")

        pull_command = f"adb pull {file_path_in_device} {file_path_in_laptop}"
        time.sleep(2)
        result = subprocess.run(pull_command, shell=True, check=True, stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            print("Screen recording pulled successfully.")
        else:
            raise subprocess.CalledProcessError
    except (subprocess.SubprocessError, subprocess.CalledProcessError) as e:
        print(f"Error occurred during recording and pulling: {e}")
    finally:
        stop_recording.set()

def wait_for_enter():
    input("Press Enter to stop recording: ")
    stop_recording.set()

def screen_record(name: str = None):
    try:
        if is_device_connected():
            prompt_thread = threading.Thread(target=wait_for_enter)
            recording_thread = threading.Thread(target=start_recording, args=(name,))

            prompt_thread.start()
            recording_thread.start()

            recording_thread.join()
            prompt_thread.join()

            # Ensure that the prompt thread doesn't hold up the script from exiting
            if prompt_thread.is_alive():
                stop_recording.set()
        else:
            print('Connect a device..')
    except KeyboardInterrupt:
        print('Recording interrupted by user.')

if __name__ == "__main__":
    screen_record()

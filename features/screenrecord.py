import os
import subprocess
import time

from utils.checks import Checks
from utils.display import Display
from utils.filehandler import FileHandler
from utils.commands import Commands
from threading import Thread, Event


class ScreenRecord:

    def __init__(self):
        """
        Screenrecord class
        """
        self.display = Display()
        self.cmd = Commands()
        self.chk = Checks()
        self.fh = FileHandler()
        self.home = os.path.expanduser('~')

    stop_recording = Event()
    recording_process = None

    def __start_recording(self, filename: str, duration: int) -> None:
        """
        Starts the screen recording from the connected android device.
        :param filename: filename of the recording.
        :param duration: duration of the recording default 180 seconds
        """
        f_name = filename
        _file_path_in_device = f"/sdcard/{f_name}"
        _file_path_in_laptop = self.home

        try:
            _record_command = f"adb shell screenrecord --bugreport --time-limit {duration} {_file_path_in_device}"
            self.recording_process = subprocess.Popen(_record_command, shell=True)

            while not self.stop_recording.is_set() and self.recording_process.poll() is None:
                if not self.chk.is_device_connected():
                    raise subprocess.SubprocessError('Device is disconnected....')
                time.sleep(1)  # Adjust sleep duration as needed

            if self.stop_recording.is_set():
                self.recording_process.terminate()
                self.recording_process.wait()

            if (self.recording_process.returncode != 0 and
                    self.recording_process.returncode != -15 and self.recording_process.returncode != -2):
                raise subprocess.SubprocessError(
                    f"Recording process returned non-zero exit status: {self.recording_process.returncode}")

        except KeyboardInterrupt:
            self.recording_process.terminate()

        except subprocess.SubprocessError as e:
            self.display.error_Exit("Failed to capture the recording", str(e))

        except Exception as e:
            self.display.error_Exit('Failed to capture the recording', str(e))

        _pull_command = f"adb pull {_file_path_in_device} {_file_path_in_laptop}"
        try:
            time.sleep(2)
            _result = subprocess.run(_pull_command, shell=True, check=True, stdout=subprocess.DEVNULL)
            if _result.returncode == 0:
                self.display.success("Screen recording pulled successfully.")
            else:
                raise subprocess.CalledProcessError
        except subprocess.CalledProcessError as e:
            self.display.error(f"Failed to pull screen recording", str(e))

    def __stop_recording(self):
        """
        Stops the screen recording.
        """
        self.stop_recording.set()

    def screenrecord(self, file_name: str = None, duration: int = 180):
        """
        Screenrecord main method in ScreenRecord class.
        :param file_name: Filename to given for the screen recording. Default None
        :param duration: Duration of the screen recording.
        """
        recording_thread = None
        try:
            self.fh.moveOrCopyFiles(_extensions=['.mp4'], destination='screenrecordings')
            if self.chk.checkAdbDevices():
                if duration > 180:
                    raise subprocess.SubprocessError
                _file_name = self.fh.get_file_name(starts_with="scr", extension="mp4", file_name=file_name)
                recording_thread = Thread(target=self.__start_recording, args=(_file_name, duration))
                recording_thread.start()
                while recording_thread.is_alive():
                    input(f"Recording started with '{_file_name}', press ENTER to stop...\n")
                    break
                self.__stop_recording()
                recording_thread.join()
        except KeyboardInterrupt:
            self.__stop_recording()
            recording_thread.join()
        except subprocess.SubprocessError as e:
            self.display.error_Exit('Duration should be less than or equal to 180.', str(e))


if __name__ == "__main__":
    scr = ScreenRecord()
    scr.screenrecord('test', 10)

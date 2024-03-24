import subprocess
import threading
from datetime import datetime

stop_recording = threading.Event()
is_ctrlc_ = threading.Event()


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


def start_screen_record(screenrecord_name):
    try:
        adb_command = ["adb", "shell", "screenrecord", "--bugreport", "--output-format=h264", "-"]
        ffmpeg_command = ["ffmpeg", "-i", "-", screenrecord_name]

        adb_process = subprocess.Popen(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=adb_process.stdout, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)

        start_time = datetime.now()

        while not stop_recording.is_set():
            if adb_process.poll() is not None or ffmpeg_process.poll() is not None:
                break

        if is_ctrlc_.is_set():
            adb_process.wait()
            ffmpeg_process.wait()

        elif stop_recording.is_set():
            adb_process.terminate()
            ffmpeg_process.terminate()
            adb_process.communicate()
            ffmpeg_process.communicate()

        end_time = datetime.now()
        duration = end_time - start_time
        print(f"Screen recording stopped. Duration: {duration.total_seconds()}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        stop_recording.set()


def stop_screen_record():
    stop_recording.set()


def is_ctrlc():
    is_ctrlc_.set()


def record_screen(screenrecord_name=None):
    if screenrecord_name is None:
        screenrecord_name = f"scr_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
    recording_thread = None
    try:
        if is_device_connected():
            recording_thread = threading.Thread(target=start_screen_record, args=(screenrecord_name,))
            recording_thread.start()
            input("Press Enter to terminate the recording...\n")
            stop_screen_record()
            recording_thread.join()
        else:
            print('connect a device')
    except KeyboardInterrupt:
        is_ctrlc()
        recording_thread.join()


if __name__ == "__main__":
    record_screen()

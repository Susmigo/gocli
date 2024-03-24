import os
import shutil
from datetime import datetime

from rich.console import Console
from utils.display import Display


class FileHandler:
    """
         A class to handle file operations such as moving or copying files.
    """

    def __init__(self):
        self.console = Console()
        self.display = Display()
        self.home = os.path.expanduser('~')
        self.time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    def get_file_name(self, starts_with: str, extension: str, file_name: str = None) -> str:
        """
        Gives the file name along with the extension. if name is none it will append the current date.
        :param starts_with: name of the file to be started with.
        :param extension: extension of the file.
        :param file_name: Default None. if not given append the date to starts_with.
        :returns: filename with extension.
        """
        if file_name is None:
            file_name = starts_with + "_" + self.time
        return f"{file_name.replace(' ', '_')}.{extension}"

    def check_dir(self, folder: str) -> bool:
        """
        Checks the directory existence in the home.
        :param folder: name of the folder.
        :returns: bool
        """
        dir_path = os.path.join(self.home, folder)
        return os.path.exists(dir_path) and os.path.isdir(dir_path)

    def make_dir(self, folder: str) -> str:
        """
        Creates the directory if it is not existed in the home.
        :param folder: Name of the folder.
        :returns: folder path
        """
        path = os.path.join(self.home, folder)
        os.makedirs(path, exist_ok=True)
        return path

    def moveOrCopyFiles(self, _extensions: list, destination: str, is_copy: bool = False, _start_name: str = ""):
        """
            Move or copy files with specified extensions and starting name to a destination directory.

            Args: _extensions (List[str]): List of file extensions to be moved or copied. destination (str): The
            directory where files will be moved or copied. is_copy (bool, optional): If True, files will be
            copied instead of moved. Defaults to False. _start_name (str, optional): Only files starting with
            this prefix will be considered. Defaults to "".
        """
        destination_dir = os.path.join(self.home, destination)
        if not self.check_dir(destination_dir):
            self.make_dir(destination_dir)
        try:
            for _ in os.listdir(self.home):
                if any(_.endswith(ext) and _.startswith(_start_name) for ext in _extensions):
                    source_path = os.path.join(self.home, _)
                    destination_path = os.path.join(destination_dir, _)

                    # check before the file exists in the destination directory
                    if os.path.exists(destination_path):
                        rename_file = f"{os.path.splitext(_)[0]}_{self.time}{os.path.splitext(_)[1]}"
                        destination_path = os.path.join(destination_dir, rename_file)

                    self.console.print("Existing file:")
                    if is_copy:
                        shutil.copy(source_path, destination_path)
                        self.display.info(f'{_} copied to {destination_path}\n')
                    else:
                        try:
                            shutil.move(source_path, destination_path)
                            self.display.info(f'{_} moved to {destination_path}\n')
                        except shutil.Error as e:
                            self.display.error('File already exists...', trace=str(e))
        except FileNotFoundError as e:
            self.display.error('File not found...', trace=str(e))


if __name__ == "__main__":
    hf = FileHandler()
    res = hf.check_dir('lol')
    print(res)
    print(hf.make_dir('lol'))
    hf.moveOrCopyFiles(['.png'], destination="screenshots")
    print(hf.get_file_name('scr', 'mp4'))

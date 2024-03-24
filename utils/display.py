import sys
from typing import Any

from rich.console import Console


class Display:
    """
    Display the user messages like errors, interrupts and success.
    """

    def __init__(self):
        self.console = Console()

    def error(self, error_msg: str, trace: str = "") -> None:
        """
        Displays the user given error msg
        :param error_msg: error msg given by user
        :param trace: trace message
        """
        self.console.print("ERROR :exclamation: : " + error_msg + f"\n{trace}", style="italic bold red", emoji=True,
                           new_line_start=True)

    def info(self, info_msg: str) -> None:
        """
         Displays info message.
         :param info_msg: Info messages to be printed.

         :returns: None
        """
        self.console.print("INFO :information_desk_person: : " + info_msg, style="italic", emoji=True,
                           new_line_start=True)

    def success(self, info_msg: str) -> None:
        """
         Displays success message.
         :param info_msg: Info messages to be printed.

         :returns: None
        """
        self.console.print("SUCCESS :rocket: : " + info_msg, style="bold green", emoji=True, new_line_start=True)

    def interrupt(self, interrupt_msg: str) -> None:
        """
        Displays success message.
         :param interrupt_msg: Interrupt messages to be printed.

         :returns: None
        """
        self.console.print("INTERRUPT :grey_exclamation: : " + interrupt_msg, style="bold yellow", emoji=True,
                           new_line_start=True)
        sys.exit(1)

    def error_Exit(self, error_msg: str, trace: str = "") -> Any:
        """
        Displays the user given error msg and exit.
        :param error_msg: error msg given by user
        :param trace: trace message

        :returns: Any
        """
        self.console.print("ERROR :bangbang: : " + error_msg + f"\n{trace}", style="italic bold red", emoji=True,
                           new_line_start=True)
        sys.exit(1)


if __name__ == "__main__":
    d = Display()
    d.console.print("hi")
    d.error("Error something went wrong", trace="print failed")
    d.info("info message")
    d.success("success done")
    d.error_Exit("Exiting done", trace="user not found")

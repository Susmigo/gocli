"""
Main Runner script for Go CLI
"""
import typer
from rich.console import Console
from pyperclip import copy
from typing_extensions import Annotated
from typing import Any

from bugdescriptor import TableFormatter, Descriptor
from bugreportgenerator import Bugreport
from utilities import checkAdbDevices

__EPILOG__ = "Made by Govardhan with :heart:"
__VERSION__ = "1.0"

app = typer.Typer(help="Go Command line interface all-in-one. :zap:", rich_markup_mode="rich", epilog=__EPILOG__)
console = Console()


def __printer(_app: Any):
    output = _app
    copy(output)
    console.print(output)


@app.command(short_help="Generates the bug description.", epilog=__EPILOG__)
def bug(wb: Annotated[
    bool, typer.Option(prompt="Do you want bugreport", )]):
    """
    Generates Bug description from the device.
    """
    if wb:
        checkAdbDevices()
        console.print("Generating Description along with Bugreport...\n")
        __printer(Descriptor.bugDescriptor())
        Bugreport.captureBugReport()
    else:
        console.print(TableFormatter.bugTableFormatter())


@app.command()
def comment(wb: bool = False):
    if wb:
        __printer(Descriptor.commentDescriptor())
        Bugreport.captureBugReport()
    else:
        __printer(Descriptor.commentDescriptor())


@app.command(short_help="Generates the bugreport from the connected device.", epilog=__EPILOG__)
def bugreport():
    Bugreport.captureBugReport()


if __name__ == "__main__":
    app()

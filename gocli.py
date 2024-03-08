"""
Main Runner script for Go CLI
"""
import time
from typing import Any

import click
import typer
from pyperclip import copy
from rich.console import Console
from typing_extensions import Annotated, Optional

from bugdescriptor import Descriptor
from bugreportgenerator import Bugreport
from cliconstants import Gocli, Bug, Comment
from devicedetails import DeviceDetails
from utilities import checkAdbDevices
from webparser import WebParser
from typer.core import TyperGroup as TyperGroupBase


def adbCheck():
    checkAdbDevices()


class TyperGroup(TyperGroupBase):
    """Custom TyperGroup class."""

    def get_usage(self, ctx: click.Context) -> str:
        """Override get_usage."""
        usage = super().get_usage(ctx)
        message = (
            f"{Gocli.TYPER_HELP_USAGE}\n\n{DeviceDetails.finalPrint()}\n\n{usage}"
        )
        return message


app = typer.Typer(rich_markup_mode="rich", epilog=Gocli.EPILOG, no_args_is_help=True,
                  context_settings={"help_option_names": ["-h", "--help"]},
                  invoke_without_command=True, cls=TyperGroup)
console = Console()


def __printer(_app: Any):
    """
    Prints the Output from any method into the terminal and also copies the output.
    :param _app: Any
    """
    output = _app
    copy(output)
    console.print(output)


def version_callback(value: bool):
    """
    Callbacks the version and exits the cli.
    :param value: bool
    """
    if value:
        console.print(Gocli.VERSION_TEXT, Gocli.VERSION, "\n", Gocli.EPILOG)
        raise typer.Exit()


# noinspection PyUnusedLocal
@app.command(name="bug", short_help=Bug.SHORT_HELP, epilog=Gocli.EPILOG)
def bugDescriptor(withbugreport: Annotated[
    bool, typer.Option("--with-bugreport", "-w",
                       help=Bug.BUGREPORT_FLAG_HELP, show_default=False,
                       )] = False,
                  export: Annotated[bool, typer.Option("--export", '-e', help=Bug.EXPORT_FLAG_HELP, )] = False,
                  version: Annotated[
                      Optional[bool], typer.Option("--version", "-v", callback=version_callback,
                                                   help=Gocli.VERSION_FLAG_HELP,
                                                   is_eager=True)] = None, ):
    """
    Generates Bug description from the Connected Android device 📲.

    --with-bugreport, -wb: Include a bug report in the output.
    --export, -e: Exports the Bug Description to buganizer.

    Examples:
    $ gocli bug --with-bugreport
    $ gocli bug -w
    $ gocli bug --export
    $ gocli bug -e
    $ gocli bug -we  [Recommended]  # Generates bugreport, also exports bug description
    """
    if withbugreport:
        console.print(Bug.WITH_BUGREPORT)
    else:
        console.print(Bug.WITHOUT_BUGREPORT)
    fo = Descriptor.bugDescriptor()
    __printer(fo)
    if export:
        WebParser.takeMetoBuganizer(fo)
        time.sleep(2)
    if withbugreport:
        Bugreport.captureBugReport()


# noinspection PyUnusedLocal
@app.command(name="cmt", short_help=Comment.SHORT_HELP, epilog=Gocli.EPILOG)
def commentDescriptor(withbugreport: Annotated[
    bool, typer.Option("--with-bugreport", "-w", help=Comment.BUGREPORT_FLAG_HELP, show_default=False)] = False,
                      export: Annotated[bool, typer.Option("--export", '-e', help=Comment.EXPORT_FLAG_HELP, )] = False,
                      version: Annotated[
                          Optional[bool], typer.Option("--version", "-v", callback=version_callback,
                                                       help=Gocli.VERSION_FLAG_HELP,
                                                       is_eager=True)] = None, ):
    """
    Generates Comment description from the Connected Android device 📲.

    --with-bugreport, -wb: Include a bug report in the output.
    --export, -e: Exports the Comment Description to buganizer.

    Examples:
    $ gocli cmt --with-bugreport
    $ gocli cmt -w
    $ gocli cmt --export
    $ gocli cmt -e
    $ gocli cmt -we  [Recommended]  # Generates bugreport, also exports Comment description.
    """
    if withbugreport:
        console.print(Comment.WITH_BUGREPORT)
    else:
        console.print(Comment.WITHOUT_BUGREPORT)
    fo = Descriptor.commentDescriptor()
    __printer(fo)
    if export:
        WebParser.takeMetoBuganizer(fo)
        time.sleep(2)
    if withbugreport:
        Bugreport.captureBugReport()


if __name__ == "__main__":
    app()
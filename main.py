"""
Main Runner script for Go CLI
"""
import typer
from rich.console import Console

from bugdescriptor import TableFormatter
from utilities import check_adb_devices
from versionmanager import Test

app = typer.Typer()
console = Console()


@app.command(short_help="Generates the bug description.")
def describeBug(with_bugreport: bool = False):
    if with_bugreport:
        console.print("taking bugreport")
    else:
        console.print(TableFormatter.tableFormatter())


@app.command(short_help="Generates the bugreport from the connected device.")
def bugreport():
    check_adb_devices()


@app.command(short_help="Generates details about the installed applications.")
def listapps(all: bool = False):
    console.print('Generating......')
    if all:
        Test.runner()


if __name__ == "__main__":
    app()

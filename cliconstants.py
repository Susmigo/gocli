class Gocli:
    TYPER_HELP = ":rocket: [bold][italic]Go Command Line Interface All-in-One.[/italic][/bold] :rocket:"
    TYPER_HELP_USAGE = " 🚀 Go Command Line Interface All-in-One. 🚀 "
    EPILOG = "Made by Govardhan with :heart:"
    VERSION = "1.0"
    VERSION_TEXT = "\n[bold][italic]Go CLI Version[/italic][/bold] :star: :"
    VERSION_FLAG_HELP = "Prints the Version."


class Bug:
    SHORT_HELP = "Generates the Bug Description from the connected device."
    WITH_BUGREPORT = "Generating Bug Description along with Bugreport...\n"
    WITHOUT_BUGREPORT = "Generating Bug Description...\n"
    BUGREPORT_FLAG_HELP = "Captures the Bug Report."
    EXPORT_FLAG_HELP = "Exports the Bug Description to Buganizer."


class Comment:
    SHORT_HELP = "Generates the Comment Description from the connected device."
    WITH_BUGREPORT = "Generating Comment Description along with Bugreport...\n"
    WITHOUT_BUGREPORT = "Generating Comment Description...\n"
    EXPORT_FLAG_HELP = "Captures the Bug Report."
    BUGREPORT_FLAG_HELP = "Exports the Comment Description to Buganizer."
    BUG_ID_FOR_COMMENT = "\nEnter the bug ID :beetle: for adding a comment"


class BugReport:
    SHORT_HELP = "Generates the Bug report."
    CONSOLE_PRINT = "Generating the Bugreport..."


class Screenshot:
    SHORT_HELP = "Captures the screenshot."
    CONSOLE_PRINT = "Capturing the screenshot."


class Screenrecord:
    SHORT_HELP = "Captures the screenrecord."
    CONSOLE_PRINT = "Capturing the screenrecord."


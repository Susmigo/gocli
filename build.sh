#!/bin/bash

install_python() {
    echo "Python not found. Installing..."

    # Check the platform and install using the appropriate package manager
    if [ "$(uname)" == "Darwin" ]; then
        # macOS
        if command -v brew &>/dev/null; then
            brew install python
        else
            echo "Homebrew is not installed. Please install it and run the script again."
            exit 1
        fi
    elif [ "$(expr substr "$(uname -s)" 1 5)" == "Linux" ]; then
        # Linux
        if command -v apt-get &>/dev/null; then
            sudo apt-get update
            sudo apt-get install -y python
            sudo apt install python3.11-venv
        else
            echo "apt-get is not available. Please install it and run the script again."
            exit 1
        fi
    else
        echo "Unsupported operating system."
        exit 1
    fi

    echo "Python has been installed successfully."
}

check_python() {
    if command -v python3 &>/dev/null; then
        echo "Python is already installed."
        echo "Installing venv"
        sudo apt install python3.11-venv
    else
        install_python
    fi
}

create_and_activate_venv() {
    VENV_DIR="$HOME/gocli"

    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment 'gocli' in the home directory..."
        python3 -m venv "$VENV_DIR"
    fi

    echo "Activating virtual environment 'gocli'..."
    source "$VENV_DIR/bin/activate"
    echo "Virtual environment 'gocli' activated."
}

fetch_files_from_git() {
    REPO_URL="https://github.com/susmigo/gocli.git"  # Replace with your Git repository URL
#    FILE_EXTENSIONS=("txt" "py" "md")  # Replace with the list of file extensions you want to fetch

    echo "Fetching files from Git repository..."
    git clone "$REPO_URL" temp_repo

    echo "Copying specified files to the virtual environment..."
#    for ext in "${FILE_EXTENSIONS[@]}"; do
#        find "temp_repo" -name "*.$ext" ! -path "temp_repo/bin/*" ! -path "temp_repo/lib/*" ! -path "temp_repo/include/*" -exec cp -r {} "$VENV_DIR/" \;
#    done
    find "temp_repo" -mindepth 1 -maxdepth 1 ! -path "temp_repo/bin/*" ! -path "temp_repo/lib/*" ! -path "temp_repo/include/*" -exec cp -r {} "$VENV_DIR/" \;


    echo "Cleaning up..."
    rm -rf temp_repo
}

install_requirements() {
    echo "Changing into 'gocli' directory..."
    cd "$VENV_DIR" || exit 1

    echo "Updating Pip..."
    pip3 install --upgrade pip

    echo "Installing requirements..."
    # Assuming requirements.txt is present in the repository, adjust as needed
    pip3 install -r requirements.txt

    echo "Installing PyInstaller..."
    pip3 install pyinstaller

    echo "Cleaning up..."
    cd ..
}

build_onefile() {
    echo "Changing into 'gocli' directory..."
    cd "$VENV_DIR" || exit 1

    echo "Building one file using PyInstaller..."
    pyinstaller  --clean gocli.py -D -F

    echo "Cleaning up..."
    cd ..
}

move_executable() {
    TEMP_FOLDER="$HOME/gocli_temp"

    echo "Creating temporary folder in home directory..."
    mkdir -p "$TEMP_FOLDER"

    echo "Moving 'gocli' executable from 'dist' to temporary folder..."
    if [ -f "$VENV_DIR"/dist/gocli ]; then
        mv "$VENV_DIR"/dist/gocli "$TEMP_FOLDER/"
    else
        echo "Error: 'gocli' file not found in 'dist' directory."
        exit 1
    fi

    echo "Deleting all files in the 'gocli' directory..."
    rm -rf "$VENV_DIR"/gocli/*

    echo "Cleaning up..."
    rm -rf "$VENV_DIR"/*

    echo "Moving 'gocli' executable from temporary folder to 'gocli' directory..."
    mv "$TEMP_FOLDER"/gocli "$VENV_DIR/"

    echo "Cleaning up..."
    rm -rf "$TEMP_FOLDER"
}

export_path_to_shell_profile() {
    echo "Exporting 'gocli' path to shell profiles..."

    VENV_DIR="$HOME/gocli"

   # Check if 'gocli' is in $PATH
    if ! command -v gocli &>/dev/null; then
        # Export the virtual environment path to .bash_profile
        echo "export PATH=\"$VENV_DIR:\$PATH\"" >> "$HOME/.bash_profile"
        echo "export PATH=\"$VENV_DIR:\$PATH\"" >> "$HOME/.bashrc"

        # Export the virtual environment path to .zprofile
        echo "export PATH=\"$VENV_DIR:\$PATH\"" >> "$HOME/.zprofile"
        echo "export PATH=\"$VENV_DIR:\$PATH\"" >> "$HOME/.zshrc"
    else
        echo "'gocli' is already in the PATH. Skipping path export."
    fi

    # Reloading the shell to apply changes
    echo "Restart the terminal..."
}

check_python
create_and_activate_venv
fetch_files_from_git
install_requirements
build_onefile
move_executable
export_path_to_shell_profile


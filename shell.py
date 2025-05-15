from colorama import Fore, Style
import subprocess
import shutil
import time
import sys
import os

history = []
current_directory = os.getcwd()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def change_directory(path):
    global current_directory
    try:
        os.chdir(path)
        current_directory = os.getcwd()
    except FileNotFoundError:
        print(Fore.RED + f"Directory not found: {path}" + Style.RESET_ALL)

def list_directory():
    for item in os.listdir():
        print(item)

def make_directory(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        print(Fore.RED + f"Directory '{name}' already exists!" + Style.RESET_ALL)

def delete_file(name):
    try:
        os.remove(name)
    except FileNotFoundError:
        print(Fore.RED + f"File '{name}' not found!" + Style.RESET_ALL)
    except IsADirectoryError:
        print(Fore.RED + f"'{name}' is a directory! Use 'rmdir' instead." + Style.RESET_ALL)

def delete_directory(name):
    try:
        shutil.rmtree(name)
    except FileNotFoundError:
        print(Fore.RED + f"Directory '{name}' not found!" + Style.RESET_ALL)

def copy_file(src, dest):
    try:
        shutil.copy(src, dest)
    except FileNotFoundError:
        print(Fore.RED + f"Source file '{src}' not found!" + Style.RESET_ALL)

def move_file(src, dest):
    try:
        shutil.move(src, dest)
    except FileNotFoundError:
        print(Fore.RED + f"Source '{src}' not found!" + Style.RESET_ALL)

def execute_command(command):
    global history
    history.append(command)
    tokens = command.split()
    if not tokens:
        return
    cmd = tokens[0].lower()

    if cmd == "cd" and len(tokens) > 1:
        change_directory(tokens[1])
    elif cmd == "dir":
        list_directory()
    elif cmd == "mkdir" and len(tokens) > 1:
        make_directory(tokens[1])
    elif cmd == "del" and len(tokens) > 1:
        delete_file(tokens[1])
    elif cmd == "rmdir" and len(tokens) > 1:
        delete_directory(tokens[1])
    elif cmd == "copy" and len(tokens) > 2:
        copy_file(tokens[1], tokens[2])
    elif cmd == "move" and len(tokens) > 2:
        move_file(tokens[1], tokens[2])
    elif cmd == "echo" and len(tokens) > 1:
        print(" ".join(tokens[1:]))
    elif cmd == "cls":
        clear_screen()
    elif cmd == "exit":
        print(Fore.YELLOW + "Exiting shell..." + Style.RESET_ALL)
        sys.exit(0)
    elif cmd == "history":
        for i, cmd in enumerate(history):
            print(f"{i}: {cmd}")
    elif cmd.startswith("!"):
        try:
            index = int(cmd[1:])
            execute_command(history[index])
        except (ValueError, IndexError):
            print(Fore.RED + "Invalid history reference!" + Style.RESET_ALL)
    else:
        try:
            subprocess.run(command, shell=True)
        except Exception as e:
            print(Fore.RED + f"Error executing command: {e}" + Style.RESET_ALL)

def shell():
    print(Fore.CYAN + "Welcome to Custom Windows Shell! Type 'help' for commands." + Style.RESET_ALL)
    while True:
        try:
            command = input(Fore.GREEN + f"{current_directory}> " + Style.RESET_ALL).strip()
            execute_command(command)
        except KeyboardInterrupt:
            print("\n" + Fore.YELLOW + "Exiting shell..." + Style.RESET_ALL)
            break

if __name__ == "__main__":
    shell()
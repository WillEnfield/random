import os
import txtcompiler

working_dir = "C:\\" 

def get_selected_dir(working_dir, command_dir):
    if command_dir == "" or command_dir == None:
        return working_dir
    if command_dir == "..":
        return os.path.dirname(working_dir)
    elif os.path.isabs(command_dir):
        return command_dir
    else:
        return os.path.join(working_dir, command_dir)

def open_file(working_dir, command):
    file = get_selected_dir(working_dir, command[5:].strip())
    if os.path.exists(file):
        if os.path.isfile(file):
            os.startfile(file)
        else:
            print("The selected path is a directory, not a file.")
    else:
        print("That's not a valid path.")

def change_dir(working_dir, command):
    new_working_dir = get_selected_dir(working_dir, command[3:].strip())
    if os.path.exists(new_working_dir):
        if not os.path.isfile(new_working_dir):
            new_working_dir = os.path.abspath(new_working_dir)
        else:
            print("Cannot select a file, please select a directory.")
    else:
        print("That's not a valid path.")
    return new_working_dir

def list_dir(working_dir, command):
    dir_path = get_selected_dir(working_dir, command[4:].strip())
    if os.path.exists(dir_path):
        try:
            dirs = os.listdir(dir_path)
        except PermissionError:
            print("Permission denied.")
            return
        if not os.path.isfile(dir_path):
            print("Contents of " + dir_path + ":")
            for item in dirs:
                if os.path.isdir(os.path.join(dir_path, item)):
                    print("<DIR> " + item)
                else:
                    print("      " + item)
        else:
            print("The selected path is a file, not a directory.")
    else:
        print("That's not a valid path.")

def run_txt(working_dir, command):
    file_path = get_selected_dir(working_dir, command[7:].strip())
    if os.path.exists(file_path):
        if os.path.isfile(file_path) and file_path.endswith(".txt"):
            with open(file_path, 'r') as file:
                code = file.read()
                with open(file_path, 'r') as f:
                    txtcompiler.txt_compiler(f)
        else:
            print("The selected path is not a .txt file.")
    else:
        print("That's not a valid path.")


while True:
    command = input(working_dir + "> ")
    if command == "help":
        print("""Commands:
        'help' - show this message
        'open (path)'- open the file in the default program
        'end' - end the program
        'cd (path)' - select a new path
        'dir (path)*' - List the content of the directory
        'runtxt (path)' - run a .txt file as described in 'txtdocs'
        'txtdocs' - show documentation for running .txt files
        *optional""")
    elif command == "end":
        break
    elif command.startswith("open "):
        open_file(working_dir, command)
    elif command.startswith("cd "):
        working_dir = change_dir(working_dir, command)
    elif command == "":
        continue
    elif command.startswith("dir"):
        list_dir(working_dir, command)
    elif command == "txtdocs":
        os.startfile("C:\\work\\random\\reader\\txtdocs.html")
    elif command.startswith("runtxt "):
        run_txt(working_dir, command)
    else:
        print("Unknown command. Type 'help' for a list of commands.")
import os

workingdir = "C:\\" 
def open_file(workingdir, command):
    if os.path.isabs(command[5:].strip()):
        file = command[5:].strip()
    else:
        file = os.path.join(workingdir, command[5:].strip())
    if os.path.exists(file):
        if os.path.isfile(file):
            os.startfile(file)
        else:
            print("The selected path is a directory, not a file.")
    else:
        print("That's not a valid path.")

def changedir(workingdir, command):
    if command[3:].strip() == "..":
        new_workingdir = os.path.dirname(workingdir)
    elif os.path.isabs(command[3:].strip()):
        new_workingdir = command[3:].strip()
    else:
        new_workingdir = os.path.join(workingdir, command[3:].strip())
    if os.path.exists(new_workingdir):
        if not os.path.isfile(new_workingdir):
            workingdir = os.path.abspath(new_workingdir)
        else:
            print("Cannot select a file, please select a directory.")
    else:
        print("That's not a valid path.")
    return workingdir

def dir(workingdir, command):
    if len(command) == 3:
        print("Contents of " + workingdir + ":")
        for item in os.listdir(workingdir):
            print(item)
    else:
        if os.path.isabs(command[4:].strip()):
            dir_path = command[4:].strip()
        else:
            dir_path = os.path.join(workingdir, command[4:].strip())
        if os.path.exists(dir_path):
            if not os.path.isfile(dir_path):
                print("Contents of " + dir_path + ":")
                for item in os.listdir(dir_path):
                    print(item)
            else:
                print("The selected path is a file, not a directory.")
        else:
            print("That's not a valid path.")

while(True):
    command = input(workingdir + "> ")
    if command == "help":
        print("Commands:\nhelp - show this message\nopen (path)- open the file in the default program\nend - end the program\ncd (path) - select a new path\ndir (path)* - List the content of the directory\n *optional")
    elif command == "end":
        break
    elif command.startswith("open "):
        open_file(workingdir, command)
    elif command.startswith("cd "):
        workingdir = changedir(workingdir, command)
    elif command == "":
        continue
    elif command.startswith("dir"):
        dir(workingdir, command)
    else:
        print("Unknown command. Type 'help' for a list of commands.")
import os

path = "C:\\" 
while(True):
        command = input(path + "> ")
        if command == "help":
            print("Commands:\nhelp - show this message\nopen - open the file in the default editor\nend - end the program\nselect (path) - select a new file")
        elif command == "end":
            break
        elif command == "open":
            os.startfile(path)
        elif command.startswith("cd "):
            if path == "..":
                newpath = os.path.dirname(path)
            elif os.path.isabs(command[3:].strip()):
                new_path = command[3:].strip()
            else:
                new_path = os.path.join(os.path.dirname(path), command[3:].strip())
            if os.path.exists(new_path):
                path = os.path.abspath(new_path)
            else:
                print("That's not a valid path.")
        elif command == "":
            continue
        else:
            print("Unknown command. Type 'help' for a list of commands.")
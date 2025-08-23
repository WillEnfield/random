import subprocess

path = None
while(True):
    if path == None:
        path = input("What file do you want to select?\n")
        try:
            with open(path, 'r') as file:
                pass
        except FileNotFoundError:
            print("Thats not a valid path.")
            path = None
        else:
            if path[-4:] != ".txt":
                print("Thats not a txt file. Please select a txt file.")
                path = None
    else:
        pass
        #once file is selected we go here


with open(path, 'r') as file:
    content = file.read()
    print(content)
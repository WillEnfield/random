path = input("What so you want to read?\n")
with open(path, 'r') as file:
    content = file.read()
    print(content)
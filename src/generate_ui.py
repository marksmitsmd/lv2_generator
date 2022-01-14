# script to generate the UI portion of a DISTRHO plugin

print("generate_ui imported")

def generate_file(path, name):
    new_file = open(path + f"/UI{name}.cpp", "w")
    new_file.write("//This file was automatically generated.\n\n")
    new_file.write("//UI code would go here.\n\n")
    new_file.close()

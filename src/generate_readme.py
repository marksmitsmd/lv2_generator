# script to generate a readme file for a DITRHO plugin

print("generate_readme imported")

def generate_file(path, name):
    new_file = open(path + "/README.md", "w")
    new_file.write("This file was automatically generated.\n")
    new_file.write("Plugin: " + name + " readme:\n")
    new_file.close()

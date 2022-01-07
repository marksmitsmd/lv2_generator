import os
import generate_makefile
import generate_plugin_info
import generate_plugin
import generate_ui
import generate_readme

# get plugin name

plugin_name = raw_input("Enter plugin name: ")
#TODO: add execption handling for bad input

# generate folder structure

'''
bin folder
    <Name>
        CMakeLists.txt
        DistrhoPluginInfo.h
        Plugin<Name>.cpp ~.hpp
        UI<Name>.cpp ~.hpp
        Makefile
        README.md
'''

path_to_script = os.path.dirname(os.path.realpath(__file__))
path_to_bin = os.path.dirname(path_to_script) + "/bin"
try: os.mkdir(path_to_bin)
except: print("bin directory already exists")

path_to_plugin = path_to_bin + "/" + plugin_name
try: os.mkdir(path_to_plugin)
except: print("plugin directory already exists and will be overwritten")

# generate the files

generate_readme.generate_file(path_to_plugin, plugin_name)
generate_plugin_info.generate_file(path_to_plugin, plugin_name)
generate_makefile.generate_file(path_to_plugin, plugin_name)
generate_plugin.generate_files(path_to_plugin, plugin_name)

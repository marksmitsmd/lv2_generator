import os

# generate folder structure

'''
bin folder
    <Name>
        CMakeLists.txt
        DistrhoPluginInfo.h
        <Name>PluginParameters.cpp
        <Name>UIParameters.cpp
        Makefile
        README.md
'''

os.mkdir("../bin")
f = open("../bin/README.md", "w")
f.write("This file was automatically generated.")
f.close()

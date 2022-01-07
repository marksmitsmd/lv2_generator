print("generate_makefile imported")

make_lines_1 = [
"#!/usr/bin/make -f",
"# Makefile for DISTRHO Plugins #",
"# ---------------------------- #",
"# Created by falkTX, Christopher Arndt, and Patrick Desaulniers",
"",
"# -------------------------------------------------------------",
"# Project name, used for binaries"
]

make_lines_2 = [
"# -------------------------------------------------------------",
"# Run general makefile definitions for DPF plugins",
"",
"include ../../Makefile.plugins.mk", #might want to split this dependency
"",
"BUILD_CXX_FLAGS += -I../../../imgui -I../../../imgui/backends",
"BUILD_CXX_FLAGS += $(shell $(PKG_CONFIG) glew --cflags)",
"LINK_FLAGS += $(shell $(PKG_CONFIG) glew --libs)",
"",
"# -------------------------------------------------------------",
"# Enable all selected plugin types",
"",
"ifeq ($(HAVE_OPENGL),true)",
"",
"TARGETS += jack",
"",
"ifneq ($(MACOS_OR_WINDOWS),true)",
"ifeq ($(HAVE_LIBLO),true)",
"TARGETS += dssi",
"endif",
"endif",
"",
"TARGETS += lv2_sep",
"TARGETS += vst",
"",
"endif",
"",
"all: $(TARGETS)",
"",
"# -------------------------------------------------------------"
]

user_lines = []

def generate_lines_from_input(name):
    user_lines.append("NAME = d_" + str(name))
    user_lines.append("")
    user_lines.append("# -------------------------------------------------------------")
    user_lines.append("# Files to build")
    user_lines.append("")
    user_lines.append("FILES_DSP = \\")
    user_lines.append("\tPlugin" + str(name) + ".cpp")
    user_lines.append("")
    user_lines.append("FILES_UI = \\")
    user_lines.append("\tUI" + str(name) + ".cpp")

def generate_file(path, name):
    new_file = open(path + "/Makefile", "w")

    new_file.write("# This file was automatically generated.\n\n")

    for line in make_lines_1:
        new_file.write(line + "\n")
    new_file.write("\n")

    generate_lines_from_input(name)
    for line in user_lines:
        new_file.write(line + "\n")
    new_file.write("\n")

    #TODO what to do with makefile includes
    for line in make_lines_2:
        new_file.write(line + "\n")
    new_file.write("\n")

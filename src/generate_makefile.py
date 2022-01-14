# script to generate a makefile for a DITRHO plugin

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
"TARGETS += lv2_dsp",
"TARGETS += vst",
"",
"endif",
"",
"all: $(TARGETS)",
"",
"# -------------------------------------------------------------",
"# Mod specific build instructions",
"# NOTE: note path must be absolute",
"MOD_WORKDIR ?= $(HOME)/mod-workdir",
"MOD_ENVIRONMENT = AR=${1}/host/usr/bin/${2}-gcc-ar",
"CC=${1}/host/usr/bin/${2}-gcc",
"CPP=${1}/host/usr/bin/${2}-cpp",
"CXX=${1}/host/usr/bin/${2}-g++",
"LD=${1}/host/usr/bin/${2}-ld",
"PKG_CONFIG=${1}/host/usr/bin/pkg-config",
"STRIP=${1}/host/usr/bin/${2}-strip",
"CFLAGS=\"I${1}/staging/usr/unclude\"",
"CPPFLAGS= ",
"CXXFLAGS=\"-I${1}/staging/usr/icnlude\"",
"LDFLAGS=\"-L${1}/staging/usr/lib\" \\",
"EXE_WRAPPER=\"qemu-${3}-static -L ${1}/target\"",
"",
"modduo:",
"\t$(MAKE) $(call MOD_ENVIRONMENT,$(MOD_WORKDIR)/modduo,arm-mod-linux-gnueabihf,arm)",
"",
"modduox:",
"\t$(MAKE) $(call MOD_ENVIRONMENT,$(MOD_WORKDIR)/modduox,aarch64-mod-linux-gnueabi,aarch64)",
"",
"moddwarf:",
"\t$(MAKE) $(call MOD_ENVIRONMENT,$(MOD_WORKDIR)/moddwarf,aarch64-mod-linux-gnu,aarch64)",
"",
"publish:",
"\ttar -C bin -cz $(subst bin/,,$(wildcard bin/*.lv2)) | base64 | curl -F 'package=@-' http://192.168.51.1/sdk/install && echo",
"",
"ifneq (,$(findstring modduo-,$(MAKECMDGOALS)))",
"$(MAKECMDGOALS):",
"\t$(MAKE) $(call MOD_ENVIRONMENT,$(MOD_WORKDIR)/modduo,arm-mod-linux-gnueabihf,arm) $(subst modduo-,,$(MAKECMDGOALS))",
"endif",
"",
"ifneq (,$(findstring modduox-,$(MAKECMDGOALS)))",
"$(MAKECMDGOALS):",
"\t$(MAKE) $(call MOD_ENVIRONMENT,$(MOD_WORKDIR)/modduox,aarch64-mod-linux-gnueabi,aarch64) $(subst modduox-,,$(MAKECMDGOALS))",
"endif",
"",
"ifneq (,$(findstring moddwarf-,$(MAKECMDGOALS)))",
"$(MAKECMDGOALS):",
"\t$(MAKE) $(call MOD_ENVIRONMENT,$(MOD_WORKDIR)/moddwarf,aarch64-mod-linux-gnu,aarch64) $(subst moddwarf-,,$(MAKECMDGOALS))",
"endif",
"",
"# -------------------------------------------------------------"
]

user_lines = []

def generate_lines_from_input(name):
    user_lines.append(f"NAME = d_{name}")
    user_lines.append("")
    user_lines.append("# -------------------------------------------------------------")
    user_lines.append("# Files to build")
    user_lines.append("")
    user_lines.append("FILES_DSP = \\")
    user_lines.append(f"\tPlugin{name}.cpp")
    #user_lines.append("")
    #user_lines.append("FILES_UI = \\")
    #user_lines.append(f"\tUI{name}.cpp")

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

    new_file.close()

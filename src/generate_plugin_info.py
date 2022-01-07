# script to generate a DistrhoPluginInfo header for a DITRHO plugin

print("generate_plugin_info imported")

license_lines = ["/*",
" * Simple Gain audio effect for DISTRHO Plugin Framework (DPF)",
" * SPDX-License-Identifier: MIT",
" *",
" * Copyright (C) 2021 Jean Pierre Cimalando <jp-dev@inbox.ru>",
" * Copyright (C) 2021 Filipe Coelho <falktx@falktx.com>",
" *",
" * or without fee is hereby granted, provided that the above copyright notice and this",
" * Permission to use, copy, modify, and/or distribute this software for any purpose with",
" * permission notice appear in all copies.",
" *",
" * THE SOFTWARE IS PROVIDED \"AS IS\" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD",
" * TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN",
" * NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL",
" * DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER",
" * IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN",
" * CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.",
" */"]

plugin_definition_lines = [
"NAME ",
"NUM_INPUTS ",
"NUM_OUTPUTS ",
"URI ",
"HAS_UI ",
"IS_RT_SAFE ",
"IS_SYNTH ",
"WANT_DIRECT_ACCESS",
"WANT_LATENCY ",
"WANT_MIDI_INPUT ",
"WANT_MIDI_OUTPUT ",
"WANT_PROGRAMS ",
"WANT_STATE ",
"WANT_TIMEPOS ",
]

ui_definition_lines = [
"URI DISTRHO_PLUGIN_URI \"#UI\"",
"USE_CUSTOM ",
"CUSTOM_INCLUDE_PATH ",
"CUSTOM_WIDGET_TYPE ",
"USER_RESIZABLE "
]

def generate_file(path, name):
    new_file = open(path + "/DistrhoPluginInfo.h", "w")

    new_file.write("//This file was automatically generated.\n\n")

    for line in license_lines:
        new_file.write(line + "\n")
    new_file.write("\n")

    for line in plugin_definition_lines:
        new_file.write("#define DISTRHO_PLUGIN_" + line + "\n")
    new_file.write("\n")
    #TODO implement user input

    for line in ui_definition_lines:
        new_file.write("#define DISTRHO_UI_" + line + "\n")
    #TODO implement user input

    new_file.close()

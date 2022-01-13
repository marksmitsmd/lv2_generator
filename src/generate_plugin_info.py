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

from user_input import param_dictionary as p_dict

plugin_definition_lines = [
"NAME %s" % p_dict["name"],
"NUM_INPUTS %i" % p_dict["num_inputs"],
"NUM_OUTPUTS %i" % p_dict["num_outputs"],
"URI %s" % p_dict["URI"],
"HAS_UI 0",
"IS_RT_SAFE 1",
"IS_SYNTH %i" % p_dict["is_synth"],
"WANT_DIRECT_ACCESS 0",
"WANT_LATENCY 0",
"WANT_MIDI_INPUT %i" % p_dict["midi_in"],
"WANT_MIDI_OUTPUT %i" % p_dict["midi_out"],
"WANT_PROGRAMS 1",
"WANT_STATE 0",
"WANT_TIMEPOS 0",
]

ui_definition_lines = [
"USE_NANOVG 0",
"URI DISTRHO_PLUGIN_URI \"#UI\"",
"USE_CUSTOM 0",
#"CUSTOM_INCLUDE_PATH ",
#"CUSTOM_WIDGET_TYPE ",
"USER_RESIZABLE 0"
]

def generate_file(path, name):
    new_file = open(path + "/DistrhoPluginInfo.h", "w")

    new_file.write("//This file was automatically generated.\n\n")

    new_file.write("#ifndef DISTRHO_PLUGIN_INFO_H_INCLUDED\n")
    new_file.write("#define DISTRHO_PLUGIN_INFO_H_INCLUDED\n\n")

    for line in license_lines:
        new_file.write(line + "\n")
    new_file.write("\n")

    for line in plugin_definition_lines:
        new_file.write("#define DISTRHO_PLUGIN_" + line + "\n")
    new_file.write("\n")

    # only if the plugin has a UI which it doesn't have for now

    #for line in ui_definition_lines:
    #    new_file.write("#define DISTRHO_UI_" + line + "\n")
    #TODO implement user input

    new_file.write("\n#endif")

    new_file.close()

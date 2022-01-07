# script to generate the plugin portion of a DISTRHO plugin

print("generate_plugin imported")

from generate_plugin_info import license_lines as lic

def generate_simple_getter_function(return_type, param_name, input_par, spec, return_statement):
    func = []
    func += ["\t" + str(return_type) +
    " get" + str(param_name) +
    "(" + str(input_par) + ") " +
    str(spec) + " {"]
    func += ["\t\treturn " + str(return_statement) + ";", "\t}"]
    return func

header_lines = []

def generate_header_lines(name):
    hl = header_lines
    hl.append("#ifndef PLUGIN_" + str(name).upper() + "_H")
    hl.append("#define PLUGIN_" + str(name).upper() + "_H")
    hl += ["", "#include \"DistrhoPlugin.hpp\"", ""]
    hl += ["START_NAMESPACE_DISTRHO", ""]

    hl += ["class Plugin" + str(name) + " : public Plugin", "{"]

    hl += ["public:", "\tPlugin" + str(name) + "();", "\t~Plugin" + str(name) + "();", ""]

    hl += ["protected:"]

    hl += ["\t// Information"]
    hl += generate_simple_getter_function(
    "const char*", "Label", "", "const noexcept override", "\"" + str(name) + "\"")
    hl += generate_simple_getter_function(
    "const char*", "Description", "", "const override", "\"Here goes your description\"")
    hl += generate_simple_getter_function(
    "const char*", "Maker", "", "const noexcept override", "\"example.com\"")
    hl += generate_simple_getter_function(
    "const char*", "HomePage", "", "const override",
    "\"https://exampe.com/plugins/" + str(name).lower() + "\"")
    hl += generate_simple_getter_function(
    "const char*", "License", "", "const noexcept override",
    "\"https://spdx.org/licenses/MIT\"")
    hl += generate_simple_getter_function(
    "uint32_t", "Verion", "", "const noexcept override", "d_version(0, 1, 0)")
    hl += ["\t// Go to:", "\t// http://service.steinberg.de/databases/plugin/nsf/plugIn", "\t// Get a proper UID and fill it in here:"]
    hl += generate_simple_getter_function(
    "int64_t", "UniqueId", "", "const noexcept override", "d_cconst('a', 'b', 'c', 'd')")

    hl += ["\t// Init"]

    hl += ["\t// Internal data"]

    hl += ["\t// Optional"]

    hl += ["\t// Process"]

    hl += ["private:", ""]

    hl += ["};", ""]

    hl += ["END_NAMESPACE_DISTRHO", "", "#endif"]
    return hl

implementation_lines = []

def generate_implementation_lines(name):
    implementation_lines.append("")

def generate_files(path, name):
    # header
    new_file = open(path + "/Plugin" + name + ".hpp", "w")
    new_file.write("//This file was automatically generated.\n\n")

    for line in lic:
        new_file.write(line + "\n")
    new_file.write("\n")

    header_lines = generate_header_lines(name)
    for line in header_lines:
        new_file.write(line + "\n")
    new_file.write("\n")

    new_file.close()

    # implementation
    new_file = open(path + "/Plugin" + name + ".cpp", "w")
    new_file.write("//This file was automatically generated.\n\n")

    for line in lic:
        new_file.write(line + "\n")
    new_file.write("\n")

    generate_implementation_lines(name)
    for line in implementation_lines:
        new_file.write(line + "\n")
    new_file.write("\n")

    new_file.close()

# script to generate the plugin portion of a DISTRHO plugin

print("generate_plugin imported")

from generate_plugin_info import license_lines as lic
from user_input import param_dictionary as p_dict

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
    hl.append("#ifndef PLUGIN_%s_H" % str(name).upper())
    hl.append("#define PLUGIN_%s_H" % str(name).upper())
    hl += ["", "#include \"DistrhoPlugin.hpp\"", ""]
    hl += ["START_NAMESPACE_DISTRHO", ""]

    hl += ["#ifndef MIN", "#define MIN(a,b) ( (a) < (b) ? (a) : (b) )", "#endif", ""]
    hl += ["#ifndef MAX", "#define MAX(a,b) ( (a) > (b) ? (a) : (b) )", "#endif", ""]
    hl += ["#ifndef CLAMP", "#define CLAMP(v,min,max) (MIN((max), MAX((min), (v))))", "#endif", ""]
    hl += ["#ifndef DB_CO", "#define DB_CO(g) ((g) > -90.f ? powf(10.f, (g) * 0.05f) : 0.f)", "#endif", ""]

    hl += ["class Plugin%s : public Plugin" % name, "{"]

    hl += ["public:", "\tPlugin%s();" % name, "\t~Plugin%s();" % name, ""]
    hl += ["\tenum Parameters {", "\t\tparamGain = 0,", "\t\tparamCount", "\t};", ""]

    hl += ["protected:"]

    hl += ["\t// Information"]
    hl += generate_simple_getter_function(
    "const char*", "Label", "", "const noexcept override", "\"%s\"" % name)
    hl += generate_simple_getter_function(
    "const char*", "Description", "", "const override", "\"Here goes your description\"")
    hl += generate_simple_getter_function(
    "const char*", "Maker", "", "const noexcept override", "\"example.com\"")
    hl += generate_simple_getter_function(
    "const char*", "HomePage", "", "const override",
    "\"https://exampe.com/plugins/%s\"" % str(name).lower())
    hl += generate_simple_getter_function(
    "const char*", "License", "", "const noexcept override",
    "\"https://spdx.org/licenses/MIT\"")
    hl += generate_simple_getter_function(
    "uint32_t", "Version", "", "const noexcept override", "d_version(0, 1, 0)")
    hl += ["\t// Go to:", "\t// http://service.steinberg.de/databases/plugin/nsf/plugIn", "\t// Get a proper UID and fill it in here:"]
    hl += generate_simple_getter_function(
    "int64_t", "UniqueId", "", "const noexcept override", "d_cconst('a', 'b', 'c', 'd')")
    hl += [""]

    hl += ["\t// Init"]
    hl += ["\tvoid initParameter(uint32_t index, Parameter& parameter) override;"]
    hl += ["\tvoid initProgramName(uint32_t index, String& programName) override;", ""]

    hl += ["\t// Internal data"]
    hl += ["\tfloat getParameterValue(uint32_t index) const override;"]
    hl += ["\tvoid setParameterValue(uint32_t index, float value) override;"]
    hl += ["\tvoid loadProgram(uint32_t index) override;", ""]

    hl += ["\t// Optional"]
    hl += ["\t// Optional callback to inform the plugin about a sample rate change"]
    hl += ["\tvoid sampleRateChanged(double newSampleRate) override;", ""]

    hl += ["\t// Process"]
    hl += ["\tvoid activate() override;"]

    # generate the inputs for the run function based on user input
    run_inputs = "const float**, float**"
    if p_dict["num_outputs"] > 0:
        run_inputs += " outputs, uint32_t frames"
    else:
        run_inputs += ", uint32_t"
    if p_dict["midi_in"] > 0:
        run_inputs += ", const MidiEvent* midiEvents, uint32_t midiEventCount"

    # run function generation based on user input
    hl += ["\tvoid run(%s) override;" % run_inputs, ""]

    hl += ["private:"]
    hl += ["\tfloat\tfParams[paramCount];", "\tdouble\tfSampleRate;", "\tfloat\tgain;", ""]

    hl += ["};", ""]

    hl += ["struct Preset {", "\tconst char* name;", "\tfloat params[Plugin%s::paramCount];" % name, "};", ""]
    hl += ["const Preset factoryPresets[] = {", "\t{", "\t\t\"Unity Gain\",", "\t\t{0.0f}", "\t}"]
    hl += ["\t//,{", "\t//\t\"Another preset\",\t// preset name"]
    hl += ["\t//\t{-14.f, ...}\t// array of presetCount float param values", "\t//}", "};", ""]
    hl += ["const uint presetCount = sizeof(factoryPresets) / sizeof(Preset);", ""]

    hl += ["END_NAMESPACE_DISTRHO", "", "#endif"]
    return hl

implementation_lines = []

def generate_implementation_lines(name):
    il = implementation_lines
    il += ["#include \"Plugin%s.hpp\"" % name, ""]
    il += ["START_NAMESPACE_DISTRHO", ""]

    il += ["Plugin%s::Plugin%s()" % (name, name)]
    il += ["\t : Plugin(paramCount, presetCount, 0) // paramCount params, presetCount programs, 0 states"]
    il += ["{", "\tfor (unsigned p = 0; p < paramCount; ++p) {"]
    il += ["\t\tParameter param;", "\t\t initParameter(p, param);", "\t\tsetParameterValue(p, param.ranges.def);", "\t}", "}", ""]

    il += ["Plugin%s::~Plugin%s() {" % (name, name), "", "}", ""]

    il += ["//Init"]
    il += ["void Plugin%s::initParameter(uint32_t index, Parameter& parameter) {" % name]
    il += ["\tif(index >= paramCount)", "\t\treturn;", ""]
    il += ["\tparameter.ranges.min = -90.f;", "\tparameter.ranges.max = 30.f;", "\tparameter.ranges.def = 0.f;"]
    il += ["\tparameter.unit = \"db\";", "\tparameter.hints = kParameterIsAutomable;", ""]
    il += ["\tswitch(index) {", "\t\tcase paramGain:", "\t\t\tparameter.name = \"Gain (dB)\";"]
    il += ["\t\t\tparameter.shortName = \"Gain\";", "\t\t\tbreak;", "\t}", "}", ""]

    il += ["/**", "  Set the name of the program @a index."]
    il += ["  This function will be called once, shortly after the plugin is created", "*/"]
    il += ["void Plugin%s::initProgramName(uint32_t index, String& programName) {" % name]
    il += ["\t if (index < presetCount) {", "\t\tprogramName = factoryPresets[index].name;", "\t}", "}", ""]

    il += ["//Internal data", "/**", "  Optional callback to inform the plugin of a sample rate change", "*/"]
    il += ["void Plugin%s::sampleRateChanged(double newSampleRate) {" % name]
    il += ["\tfSampleRate = newSampleRate;", "}", ""]

    il += ["/**", "  Get the current value of a parameter.", "*/"]
    il += ["float Plugin%s::getParameterValue(uint32_t index) const {" % name]
    il += ["\treturn fParams[index];", "}", ""]

    il += ["/**", "  Change a parameter value.", "*/"]
    il += ["void Plugin%s::setParameterValue(uint32_t index, float value) {" % name]
    il += ["\tfParams[index] = value;", ""]
    il += ["\tswitch(index) {", "\t\tcase paramGain:", "\t\t\tgain = DB_CO(CLAMP(fParams[paramGain], -90.0, 30.0));"]
    il += ["\t\t\tbreak;", "\t}", "}", ""]

    il += ["/**", "  Load a program.", "  The host may call this function from any context,", "  including realtime processing.", "*/"]
    il += ["void Plugin%s::loadProgram(uint32_t index) {" % name]
    il += ["\tif (index < presetCount) {", "\t\tfor (int i=0; i < paramCount; i++) {"]
    il += ["\t\t\tsetParameterValue(i, factoryPresets[index].params[i]);", "\t\t}", "\t}", "}", ""]

    il += ["//Process"]
    il += ["void Plugin%s::activate() {" % name, "\t//plugin is activated", "}", ""]

    # generate the inputs for the run function based on user input
    run_inputs = "const float**"
    if p_dict["num_inputs"] > 0:
        run_inputs += " inputs"
    run_inputs += ", float**"
    if p_dict["num_outputs"] > 0:
        run_inputs += " outputs, uint32_t frames"
    else:
        run_inputs += ", uint32_t"
    if p_dict["midi_in"] > 0:
        run_inputs += ", const MidiEvent* midiEvents, uint32_t midiEventCount"

    # run function generation based on user input
    il += ["void Plugin%s::run(%s) {" % (name, run_inputs)]

    # MIDI input handling
    if p_dict["midi_in"] > 0:
        il += ["\t// MIDI input handling"]
        il += ["\tfor (uint32_t i=0; i<midiEventCount; i++) {", "\t\t// handle midiEvents[i]", "\t}", ""]

    # audio handling
    if p_dict["num_inputs"] > 0:
        il += ["\t// assumes two inputs, the script found %i from the user input, please adjust accordingly" % p_dict["num_inputs"]]
        il += ["\t// get the left and right audio inputs"]
        il += ["\tconst float* const inpL = inputs[0];", "\tconst float* const inpR = inputs[1];", ""]
    if p_dict["num_outputs"] > 0:
        il += ["\t// assumes two outputs, the script found %i from the user input, please adjust accordingly" % p_dict["num_outputs"]]
        il += ["\t// get the left and right audio outputs"]
        il += ["\tfloat* const outL = outputs[0];", "\tfloat* const outR = outputs[1];", ""]
        if p_dict["num_inputs"] > 0:
            il += ["\t// apply gain against all samples, again assuming two ins and outs", "\tfor (uint32_t i=0; i < frames; i++) {"]
            il += ["\t\toutL[i] = inpL[i] * gain;", "\t\toutR[i] = inpR[i] * gain;", "\t}", ""]
        else:
            il += ["\t// generate output values, again assuming two outs", "\tfor (uint32_t i=0; i < frames; i++) {"]
            il += ["\t\toutL[i] = 0", "\t\toutR[i] = 0", "\t}", ""]

    # MIDI output handling
    if p_dict["midi_out"] > 0:
        il += ["\t// write MIDI events:", "\t// writeMidiEvent();", ""]

    il += ["}", ""]

    il += ["Plugin* createPlugin() {", "\treturn new Plugin%s();" % name, "}", ""]

    il += ["END_NAMESPACE_DISTRHO"]

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

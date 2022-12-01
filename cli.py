import sys
import json
import wsgi


def parseArgs(args):
    out = {}
    i = 0
    while i < len(args):
        cur_arg = args[i]
        if cur_arg.startswith("-"):
            arg_name = cur_arg.lstrip("-")
            i += 1
            arg_value = args[i]
            out[arg_name] = arg_value
        else:
            out["command"] = cur_arg
        i += 1
    return out


def loadConfig(cfg):
    with open(cfg) as f:
        cfg_dict = json.loads(f.read())
    return cfg_dict


def printHelp():
    print("help text placeholder")


if __name__ == "__main__":
    if sys.argv[1] in ["-h", "--help"]:  # User needs help
        printHelp()
        sys.exit()

    argdict = parseArgs(sys.argv[1:])  # Pass all args except filename

    if "cfg" in argdict:  # User has specified a config file to read
        config = loadConfig(argdict["cfg"])
    else:
        config = {}

    if not "command" in argdict:  # User hasn't specified any subcommand
        print("Error: no command specified!")
        sys.exit()

    if argdict["command"] == "flask":
        wsgi.runApp(config["flask"])  # Run flask app with custom config

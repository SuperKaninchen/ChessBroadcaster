import sys
import json
import wsgi

import board_calibration


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


def checkArgdict(argdict):  # Check if args contain necessary info
    if not "i" in argdict:
        sys.exit("Error: no cam index specified")
    if not "a" in argdict:
        sys.exit("Error: no cam api specified")

if __name__ == "__main__":

    # LB WAS HERE: Dude, plz use argparse in a less confusing way! ;-)
    # Check this: https://docs.python.org/3/library/argparse.html#example
    # Do NOT use sys.argv at all, do NOT implement help yourself, let argparse
    # do the magic!
    # Another (longer) example:
    # https://github.com/gandie/Ants/blob/master/bin/ants#L34

    if len(sys.argv) == 1:
        sys.exit("Error: missing arguments")
    if sys.argv[1] in ["-h", "--help"]:  # User needs help
        printHelp()
        sys.exit()

    argdict = parseArgs(sys.argv[1:])  # Parse all args except filename

    if "cfg" in argdict:  # User has specified a config file to read
        config = loadConfig(argdict["cfg"])
    else:
        checkArgdict(argdict)
        config["cam"] = {
            "index": argdict["i"],
            "api": argdict["a"]
        }

    if not "command" in argdict:  # User hasn't specified any subcommand
        sys.exit("Error: no command specified!")

    if argdict["command"] == "flask":
        wsgi.runApp(config["flask"])  # Run flask app with custom config

    elif argdict["command"] == "stream":
        pass  # Run image recognition and send updates to flask

    elif argdict["command"] == "calibrate":
        board_calibration.calibrate(config["cam"])

    else:
        sys.exit("Error: unknown command")

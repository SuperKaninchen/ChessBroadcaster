import sys


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
    pass


if __name__ == "__main__":
    if sys.argv[1] in ["-h", "--help"]:
        print("Help")
    else:
        argdict = parseArgs(sys.argv[1:])
        if "cfg" in argdict:
            loadConfig(argdict["cfg"])
        if not "command" in argdict:
            print("Error: no command specified!")
            sys.exit()
        print(argdict)

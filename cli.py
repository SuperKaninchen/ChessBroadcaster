import sys
import json
import wsgi
import argparse

import board_calibration


def loadConfig(cfg):
    with open(cfg) as f:
        cfg_dict = json.loads(f.read())
    return cfg_dict


if __name__ == "__main__":

    # LB WAS HERE: Dude, plz use argparse in a less confusing way! ;-)
    # Check this: https://docs.python.org/3/library/argparse.html#example
    # Do NOT use sys.argv at all, do NOT implement help yourself, let argparse
    # do the magic!
    # Another (longer) example:
    # https://github.com/gandie/Ants/blob/master/bin/ants#L34

    parser = argparse.ArgumentParser(description="CLI for chess broadcasting")

    parser.add_argument(  # For specifying a cam api
        "command",
        help="Specifies which subcommand to run",
        choices=["test", "calibrate", "stream", "flask"]
    )

    parser.add_argument(  # For using a config file
        "-c",
        "--config",
        help="Specifies path to a config file"
    )

    parser.add_argument(  # For specifying a cam index
        "-i",
        "--index",
        help="Specifies camera index"
    )

    parser.add_argument(  # For specifying a cam api
        "-a",
        "--api",
        help="Specifies camera API",
        choices=["any", "l4v2"]
    )

    args = parser.parse_args()

    if args.config:  # User has specified a config file to read
        config = loadConfig(args.config)
    else:
        config = {}
        config["cam"] = {
            "index": args.index,
            "api": args.api
        }

    if args.command == "flask":
        wsgi.runApp(config["flask"])  # Run flask app with custom config

    elif args.command == "stream":
        pass  # Run image recognition and send updates to flask

    elif args.command == "calibrate":
        board_calibration.calibrate(config["cam"])

    else:
        sys.exit("Error: unknown command")

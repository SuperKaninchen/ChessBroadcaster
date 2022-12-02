import sys
import json
import wsgi
import argparse

import board_calibration
import test_video


def loadConfig(cfg):
    with open(cfg) as f:
        cfg_dict = json.loads(f.read())
    return cfg_dict


def initParser(parser):
    parser.add_argument(  # For using a config file
        "-c",
        "--config",
        help="Specifies path to a config file"
    )

    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = "command"

    flask_parser = subparsers.add_parser(  # Subparser for flask command
        "flask",
        help="Start the flask server"
    )
    flask_parser.add_argument(  # For specifying flasks host address
        "-a",
        "--address",
        help="Specifies flasks host address"
    )
    flask_parser.add_argument(  # For specifying flasks host port
        "-p",
        "--port",
        help="Specifies flasks host port",
        type=int
    )

    stream_parser = subparsers.add_parser(  # Subparser for stream command
        "stream",
        help="Capture the board and stream updates to flask"
    )
    stream_parser.add_argument(  # For specifying a cam index
        "-i",
        "--index",
        help="Specifies camera index",
        type=int
    )
    stream_parser.add_argument(  # For specifying a cam api
        "-a",
        "--api",
        help="Specifies camera API",
        choices=["any", "l4v2"]
    )

    stream_parser = subparsers.add_parser(  # Subparser for calibrate command
        "calibrate",
        help="Calibrate the program"
    )
    stream_parser.add_argument(  # For specifying a cam index
        "-i",
        "--index",
        help="Specifies camera index",
        type=int
    )
    stream_parser.add_argument(  # For specifying a cam api
        "-a",
        "--api",
        help="Specifies camera API",
        choices=["any", "l4v2"]
    )

    stream_parser = subparsers.add_parser(  # Subparser for test command
        "test",
        help="Display the chosen camera stream for testing"
    )
    stream_parser.add_argument(  # For specifying a cam index
        "-i",
        "--index",
        help="Specifies camera index",
        type=int
    )
    stream_parser.add_argument(  # For specifying a cam api
        "-a",
        "--api",
        help="Specifies camera API",
        choices=["any", "l4v2"]
    )


if __name__ == "__main__":

    # LB WAS HERE: Dude, plz use argparse in a less confusing way! ;-)
    # Check this: https://docs.python.org/3/library/argparse.html#example
    # Do NOT use sys.argv at all, do NOT implement help yourself, let argparse
    # do the magic!
    # Another (longer) example:
    # https://github.com/gandie/Ants/blob/master/bin/ants#L34

    parser = argparse.ArgumentParser(description="CLI for chess broadcasting")

    initParser(parser)

    args = parser.parse_args()

    if args.config:  # User has specified a config file to read
        config = loadConfig(args.config)
    else:
        config = {}
        if args.command == "flask":
            config["flask"] = {
                "host": args.address,
                "port": args.port
            }
        else:
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

    elif args.command == "test":
        test_video.testCamera(config["cam"])  # Show camera stream for testing

    else:
        sys.exit("Error: unknown command")

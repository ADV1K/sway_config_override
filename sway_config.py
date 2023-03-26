#!/usr/bin/env python3
import logging
import os
import sys
from glob import glob
from pathlib import Path
from pprint import pprint

# Set the logger
logging.basicConfig(format="", level=logging.INFO)


def check_valid_files(*paths: str | Path):
    for path in paths:
        if not Path(path).is_file():
            raise Exception(f"Invalid File: {path}")


def include(path: str) -> dict:
    config_options = {}
    for file in glob(path):
        logging.info(f"Loading File: {file}")
        config_options.update(parse_config(file))
    return config_options


def include_one(primary_path: str, secondary_path: str) -> dict:
    config_options = {}
    imported = set()
    for file in (*glob(primary_path), *glob(secondary_path)):
        # skip the file if it has already been imported
        basename = Path(file).name
        if basename in imported:
            logging.info(f"Skipping File: {file}")
            continue

        logging.info(f"Loading File: {file}")
        config_options.update(parse_config(file))
        imported.add(basename)

    return config_options


def set_from_resource(args: list[str]):
    # Will Implement Later :P
    return args


def parse_config(file: str | Path) -> dict:
    # config details are stored in a dictionary
    config_options = {}

    # check if file exists
    path = Path(os.path.expandvars(file))
    check_valid_files(path)

    # Open file and iterate over lines
    with path.open() as f:
        for line in f:
            # skip empty lines and comments
            line = line.strip()
            if not line or line[0] == "#":
                continue

            # process commands
            cmd, *args = line.split()
            match cmd:
                # Commands
                case "include":
                    if len(args) != 1:
                        raise Exception(
                            "Command `include` takes only one argument: `path`"
                        )
                    config_options.update(include(args[0]))

                case "include_one":
                    if len(args) != 2:
                        raise Exception(
                            "Command `include_one` takes two arguments: `primary path` and `secondary path`"
                        )
                    config_options.update(include_one(args[0], args[1]))

                case "set_from_resource":
                    set_from_resource(args)

                # Probably a config option
                case _:
                    config_options[cmd] = args

    return config_options


if __name__ == "__main__":
    if len(sys.argv) == 2:
        pprint(parse_config(sys.argv[1]))
    else:
        print(f"Usage:\n\tpython3 {sys.argv[0]} CONFIG")

#!/usr/bin/env python
# coding: utf-8

import argparse
import asyncio

from pathlib import Path

from main import loop_structure, __version__
from utils.input import parse_bool
from utils.common import yes_no
from utils.display import Write

root = Path(__file__).resolve().parent
license = Path(root / "LICENSE").read_text()
desc = """
Iterate over a directory and perform compression, resizing and formatting
for optimal web capabilities.
"""
epilog = """
examples:

python3 cli.py --skip-existing false --copy true --image-formats webp ./videos
python3 cli.py --skip-existing false --video-formats webm ./videos
python3 cli.py --thumbnail --vtt --video-formats mp4 webm ./videos
python3 cli.py --video-formats mp4 webm ./videos ./go/here

A = required [A] = optional [A ...]  = optional list
"""

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter, description=desc, epilog=epilog
)

parser.add_argument(
    "-v", "--version", action="version", version="%(prog)s " + __version__
)
parser.add_argument(
    "--license", action="version", version=license, help="show program's license"
)


parser.add_argument(
    "input",
    type=Path,
    nargs="?",
    default=Path.cwd(),
    help="folder to iterate over (default: current dir)",
)
parser.add_argument(
    "output",
    type=Path,
    nargs="?",
    default=None,
    help="destination folder (default: `-copy` added to input folder)",
)

parser.add_argument(
    "--slugify",
    type=parse_bool,
    nargs="?",
    const=True,
    default=True,
    metavar="BOOL",
    help="slugify filenames (default: True)",
)
parser.add_argument(
    "--skip-existing",
    type=parse_bool,
    nargs="?",
    const=True,
    default=True,
    metavar="BOOL",
    help="skip existing processed files (default: True)",
)
parser.add_argument(
    "--gif",
    type=parse_bool,
    nargs="?",
    const=True,
    default=False,
    metavar="BOOL",
    help="process GIF´s (default: False)",
)
parser.add_argument(
    "--copy",
    type=parse_bool,
    nargs="?",
    const=True,
    default=False,
    metavar="BOOL",
    help="copy not processable files (default: False)",
)
parser.add_argument(
    "--image-formats",
    type=str,
    nargs="+",
    default=[],
    choices=["png", "jpg", "webp"],
    metavar="LIST",
    help="image types to convert to (increases the execution time)",
)
parser.add_argument(
    "--video-formats",
    type=str,
    nargs="+",
    default=[],
    choices=["mp4", "webm"],
    metavar="LIST",
    help="video types to convert to (increases the execution time)",
)
parser.add_argument(
    "--thumbnail",
    type=parse_bool,
    nargs="?",
    const=True,
    default=False,
    metavar="BOOL",
    help="create thumbnails from video files (default: False)",
)
parser.add_argument(
    "--vtt",
    type=parse_bool,
    nargs="?",
    const=True,
    default=False,
    metavar="BOOL",
    help="create video progress thumbnails (default: False)",
)

args = parser.parse_args()

if not args.output:
    args.output = Path(str(args.input) + "-copy")

Write.text("Input: {}".format(args.input))
Write.text("Output: {}".format(args.output))
proceed = yes_no("Continue?")
if not proceed:
    exit(0)
Write.line()  # empty
Write.green("Starting...")
Write.line()  # empty

args.output.mkdir(parents=True, exist_ok=True)

asyncio.run(loop_structure(args))  # start the loop

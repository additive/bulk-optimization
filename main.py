#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2019 Marvin Heilemann (marvin.heilemann+github@googlemail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import asyncio

from pathlib import Path

from utils.errors import WrongInputError
from utils.common import convert_bytes, has_transparency
from utils.display import Write, display_file_info

from generators import File, VTT, Thumbnail, MP4, WEBM, GIF, PNG, JPG, WEBP


__usage = """
Bulk Optimization

Iterate over a directory and perform compression, resizing and
formatting for optimal web capabilities.

Options:
    input_path      Where to start searching                (optional)
    output_path     Where to copy the folder structure      (optional)

Usage:
    python3 main.py
    python3 main.py /some/dir
    python3 main.py /some/dir /goes/here
"""


if sys.argv[1] and sys.argv[1] in ["help", "-h", "--help"]:
    print(__usage)
    exit(0)

current_path = Path.cwd()
Write.text("Current path is: {}".format(current_path))

input_path = Path(sys.argv[1]) if len(sys.argv) == 2 else current_path
Write.text("Input path is: {}".format(input_path))
if not input_path.is_dir():
    raise WrongInputError("Input path is not a directory!")

if len(sys.argv) == 3:
    output_path = Path(sys.argv[2])
else:
    output_path = Path(str(input_path) + "-Copy")
    output_path.mkdir(parents=True, exist_ok=True)
Write.text("Output path is: {}".format(output_path))
if not output_path.is_dir():
    raise WrongInputError("Output path is not a directory!")

Write.line()  # empty

# TODO: enable
# proceed = yes_no("Continue?")
# if not proceed:
#     exit(0)
Write.green("Starting...")
Write.line()  # empty


async def main_loop():
    input_length = len(list(Path(input_path).glob("**/*")))
    old_combined_file_size = 0
    new_combined_file_size = 0

    # Loop everything you can find in `input_path`
    for index, input_file in enumerate(Path(input_path).glob("**/*")):
        Write.yellow("Processing file {} of {}".format(index + 1, input_length))
        Write.gray(">>> ", input_file)

        # Skip all dot files, like `.DS_Store`
        if input_file.name.startswith("."):
            Write.yellow("Skipping dotfile")
            Write.line()
            continue

        # Create output directory/path
        output_file = Path(str(input_file).replace(input_path.name, output_path.name))

        # Input file is directory, create it, even if it exists and continue
        if not input_file.is_file():
            output_file.mkdir(parents=True, exist_ok=True)
            Write.blue("Skipping dir '{}'".format(input_file.name))
            Write.line()
            continue

        Write.gray("<<< ", str(output_file).replace(output_file.suffix, "..."))

        old_combined_file_size += input_file.stat().st_size

        # VIDEOS
        if input_file.suffix in {".mp4", ".wmv", ".webm", ".mov", ".vlf"}:
            input_group = "video"
            input_type = None
            display_file_info(input_group, input_type, input_file)

            # MP4
            input_type = "mp4"
            generator = MP4(input_group, input_type, input_file, output_file)
            output = await generator.run()
            display_file_info(input_group, input_type, output)

            # WEBM
            input_type = "webm"
            generator = WEBM(input_group, input_type, input_file, output_file)
            output = await generator.run()
            display_file_info(input_group, input_type, output)
            new_combined_file_size += output.stat().st_size

            # VTT
            input_type = "vtt"
            generator = VTT(input_group, input_type, input_file, output_file)
            output = await generator.run()
            display_file_info(input_group, input_type, output)

            # Thumbnail
            input_type = "thumb"
            generator = Thumbnail(input_group, input_type, input_file, output_file)
            output = await generator.run()
            display_file_info(input_group, input_type, output)

        # IMAGES
        elif input_file.suffix in {".png", ".jpeg", ".jpg", ".webp"}:
            input_group = "image"
            input_type = None
            display_file_info(input_type, input_type, input_file)

            if has_transparency(input_file):
                # PNG
                input_type = "png"
                generator = PNG(input_group, input_type, input_file, output_file)
                output = await generator.run()
                display_file_info(input_group, input_type, output)
            else:
                # JPG
                input_type = "jpg"
                generator = JPG(input_group, input_type, input_file, output_file)
                output = await generator.run()
                display_file_info(input_group, input_type, output)

            # WEBP
            input_type = "webp"
            generator = WEBP(input_group, input_type, input_file, output_file)
            output = await generator.run()
            display_file_info(input_group, input_type, output)
            new_combined_file_size += output.stat().st_size

        # GIF
        elif input_file.suffix == ".gif":
            input_group = "gif"
            input_type = None
            display_file_info(input_type, input_type, input_file)

            # GIF
            input_type = "gif"
            generator = GIF(input_group, input_type, input_file, output_file)
            output = await generator.run()
            display_file_info(input_group, input_type, output)
            new_combined_file_size += output.stat().st_size

        # All other files
        else:
            input_group = "unknown"
            input_type = None
            display_file_info(input_group, input_type, input_file)

            # Unknown
            input_type = None  # maybe use file extension here
            generator = File(input_group, input_type, input_file, output_file)
            output = await generator.run()
            display_file_info(input_group, input_type, output)
            new_combined_file_size += output.stat().st_size

        Write.text()  # empty

    Write.green("Done!")
    Write.line()
    Write.text("Old size: {}".format(convert_bytes(old_combined_file_size)))
    Write.text("New size: {}".format(convert_bytes(new_combined_file_size)))


if __name__ == "__main__":
    asyncio.run(main_loop())  # start the loop
else:
    raise ValueError("Please use the script directly, do not import it!")

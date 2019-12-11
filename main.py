import time

from pathlib import Path
from slugify import slugify

from utils.common import convert_bytes, has_transparency
from utils.display import Write, display_file_info

from generators import File, VTT, Thumbnail, MP4, WEBM, GIF, PNG, JPG, WEBP

"""
args:
    slugify:        bool
    skip_existing:  bool
    skip_gif:       bool
    no_copy:        bool
    image_formats:  list
    video_formats:  list
    no_thumbnail:   bool
    no_vtt:         bool
"""

__version__ = "1.1.0"

defaults = {"mp4": {"video_codec": "h264", "audio_codec": "aac"}}


async def loop_structure(args):
    if type(args) is not dict:
        raise ValueError("Arguments must be of type dict!")

    args.update(defaults)

    input_length = len(list(args["input"].glob("**/*")))
    old_combined_file_size = 0
    new_combined_file_size = 0
    start_time = time.time()

    # Loop every file/folder
    for index, input_file in enumerate(args["input"].glob("**/*")):
        Write.yellow("Processing file {} of {}".format(index + 1, input_length))
        Write.gray(">>> ", input_file)

        # Skip all dot files, like `.DS_Store`
        if input_file.name.startswith("."):
            Write.blue("Skipping dotfile")
            Write.line()
            continue

        # Create output directory/path
        output_file = Path(
            str(input_file).replace(str(args["input"]), str(args["output"]))
        )

        # Slugify filename
        if args["slugify"] and input_file.is_file():
            output_file = Path(
                output_file.parent,
                slugify(input_file.stem, lowercase=False) + input_file.suffix,
            )

        # Skip process if file exist already otherwise override it
        if args["skip_existing"] and output_file.exists():
            Write.blue("Skipping existing")
            Write.line()
            continue

        # Input file is directory, create it, even if it exists and continue
        if not input_file.is_file():
            output_file.mkdir(parents=True, exist_ok=True)
            Write.blue("Skipping dir '{}'".format(input_file.name))
            Write.line()
            continue

        Write.gray("<<< ", str(output_file).replace(output_file.suffix, "..."))

        old_combined_file_size += input_file.stat().st_size

        # VIDEOS
        if input_file.suffix in [".mp4", ".wmv", ".webm", ".mov", ".vlf", ".mkv"]:
            input_group = "video"
            input_type = None
            display_file_info(input_group, input_type, input_file)

            # MP4
            input_type = "mp4"
            if input_type in args["video_formats"]:
                generator = MP4(
                    input_group,
                    input_type,
                    input_file,
                    output_file,
                    args["skip_existing"],
                    args["mp4"],
                )
                output = await generator.run()
                display_file_info(input_group, input_type, output)
                new_combined_file_size += output.stat().st_size

            # WEBM
            input_type = "webm"
            if input_type in args["video_formats"]:
                generator = WEBM(
                    input_group,
                    input_type,
                    input_file,
                    output_file,
                    args["skip_existing"],
                )
                output = await generator.run()
                display_file_info(input_group, input_type, output)
                if "mp4" not in args["video_formats"]:
                    new_combined_file_size += output.stat().st_size

            # VTT
            input_type = "vtt"
            if args["vtt"]:
                generator = VTT(
                    input_group,
                    input_type,
                    input_file,
                    output_file,
                    args["skip_existing"],
                )
                output = await generator.run()
                display_file_info(input_group, input_type, output)

            # Thumbnail
            input_type = "thumb"
            if args["thumbnail"]:
                generator = Thumbnail(
                    input_group,
                    input_type,
                    input_file,
                    output_file,
                    args["skip_existing"],
                )
                output = await generator.run()
                display_file_info(input_group, input_type, output)

        # IMAGES
        elif input_file.suffix in [".png", ".jpeg", ".jpg", ".webp"]:
            input_group = "image"
            input_type = None
            display_file_info(input_type, input_type, input_file)

            if ["jpg", "png"] == sorted(args["image_formats"]):
                if has_transparency(input_file):
                    # PNG
                    input_type = "png"
                    generator = PNG(
                        input_group,
                        input_type,
                        input_file,
                        output_file,
                        args["skip_existing"],
                    )
                    output = await generator.run()
                    display_file_info(input_group, input_type, output)
                else:
                    # JPG
                    input_type = "jpg"
                    generator = JPG(
                        input_group,
                        input_type,
                        input_file,
                        output_file,
                        args["skip_existing"],
                    )
                    output = await generator.run()
                    display_file_info(input_group, input_type, output)
                    if "webp" not in args["image_formats"]:
                        new_combined_file_size += output.stat().st_size
            else:
                # PNG
                input_type = "png"
                if input_type in args["image_formats"]:
                    generator = PNG(
                        input_group,
                        input_type,
                        input_file,
                        output_file,
                        args["skip_existing"],
                    )
                    output = await generator.run()
                    display_file_info(input_group, input_type, output)
                    if not any(f in ["jpg", "webp"] for f in args["image_formats"]):
                        new_combined_file_size += output.stat().st_size
                # JPG
                input_type = "jpg"
                if input_type in args["image_formats"]:
                    generator = JPG(
                        input_group,
                        input_type,
                        input_file,
                        output_file,
                        args["skip_existing"],
                    )
                    output = await generator.run()
                    display_file_info(input_group, input_type, output)
                    if not any(f in ["png", "webp"] for f in args["image_formats"]):
                        new_combined_file_size += output.stat().st_size

            # WEBP
            input_type = "webp"
            if input_type in args["image_formats"]:
                generator = WEBP(
                    input_group,
                    input_type,
                    input_file,
                    output_file,
                    args["skip_existing"],
                )
                output = await generator.run()
                display_file_info(input_group, input_type, output)
                if not all(f in ["jpg", "png"] for f in args["image_formats"]):
                    new_combined_file_size += output.stat().st_size

        # GIF
        elif input_file.suffix == ".gif" and args["gif"]:
            input_group = "gif"
            input_type = None
            display_file_info(input_type, input_type, input_file)

            # GIF
            input_type = "gif"
            generator = GIF(
                input_group, input_type, input_file, output_file, args["skip_existing"]
            )
            output = await generator.run()
            display_file_info(input_group, input_type, output)
            new_combined_file_size += output.stat().st_size

        # All other files
        elif args["copy"]:
            input_group = "file"
            input_type = None
            display_file_info(input_group, input_type, input_file)

            # Unknown
            input_type = input_file.suffix.replace(".", "")
            generator = File(
                input_group, input_type, input_file, output_file, args["skip_existing"]
            )
            output = await generator.run()
            display_file_info(input_group, input_type, output)
            new_combined_file_size += output.stat().st_size

        else:
            Write.blue("Skipping")
            pass

        Write.text()  # empty

    elapsed_time = time.time() - start_time
    elapsed_time = round(elapsed_time // 60)
    if elapsed_time > 1:
        Write.green("Done after " + str(elapsed_time) + " minutes")
    else:
        Write.green("Done after some seconds")

    Write.line()
    Write.text("Original size: {}".format(convert_bytes(old_combined_file_size)))
    Write.text("Compressed size: {}".format(convert_bytes(new_combined_file_size)))

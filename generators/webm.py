"""
Convert a video file to web save MP4
"""

import sys
import ffmpeg

from utils.progress import show_progress
from generators.generator import Generator


class WEBM(Generator):
    async def run(self):
        self.start("Starting compression...")

        output = self.rename_extension(self.output_file, "webm")
        output.touch()  # create an empty file

        total_duration = float(ffmpeg.probe(self.input_file)["format"]["duration"])
        with show_progress(total_duration) as socket_filename:
            try:
                (
                    ffmpeg.input(self.input_file)
                    .filter("fps", fps=29, round="up")
                    .filter("scale", "min(iw,1920)", "-2")
                    .output(
                        filename=output,
                        crf=20,
                        preset="slower",
                        movflags="faststart",
                        pix_fmt="yuv420p",
                        **{"b:v": "1M", "c:v": "libvpx", "c:a": "libvorbis"}
                    )
                    .global_args("-progress", "unix://{}".format(socket_filename))
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
            except ffmpeg.Error as e:
                print(str(e.stderr, "utf-8"), file=sys.stderr)
                sys.exit(1)

        self.done()
        return output

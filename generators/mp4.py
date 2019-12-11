"""
Convert a video file to web save MP4
"""

import sys
import ffmpeg

from sty import fg

from utils.display import Box
from utils.progress import show_progress_socket
from generators.generator import Generator


class MP4(Generator):
    async def run(self):
        self.start("Starting compression...")

        output = self.rename_extension(self.output_file, "mp4")
        if output.exists() and self.skip_existing:
            self.warn("Already exists, skipping...")
            return output

        prefix = Box.new(fg.blue, "INFO") + " " + self.group_label + self.type_label
        total_duration = float(ffmpeg.probe(self.input_file)["format"]["duration"])
        with show_progress_socket(total_duration, prefix) as socket_filename:
            try:
                # BUG: video without audio results in failure: https://github.com/kkroening/ffmpeg-python/issues/204
                pipeline = ffmpeg.input(self.input_file)
                audio = pipeline.audio
                video = pipeline.video.filter("fps", fps=29, round="up").filter(
                    "scale", "min(iw,1920)", "-2"
                )
                (
                    ffmpeg.output(
                        video,
                        audio,
                        filename=output,
                        crf=24,
                        vcodec=self.options["video_codec"],
                        acodec=self.options["audio_codec"],
                        preset="slower",
                        movflags="faststart",
                        pix_fmt="yuv420p",
                        loglevel="debug",
                        **{"qscale": "3"}
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

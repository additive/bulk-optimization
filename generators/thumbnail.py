"""
Generates a compressed thumbnail for a video
"""

import ffmpeg

from generators.generator import Generator
from generators.jpg import JPG


class Thumbnail(Generator):
    async def run(self):
        self.start("Starting generator...")

        output = self.rename_extension(self.output_file, "jpg")
        output = self.rename_file(output, output.stem + "-thumb")
        output.touch()  # create an empty file

        instance = ffmpeg.input(self.input_file)
        video = instance.video

        video = video.filter("scale", "min(iw,1920)", "-2")

        stream = ffmpeg.output(
            video,
            filename=output,
            vframes=1,
            **{"hide_banner": None, "stats": None, "loglevel": "panic"}
        )

        ffmpeg.run(stream, overwrite_output=True)

        generator = JPG(self.group, self.type, output, output)
        output = await generator.run()

        self.done()
        return output

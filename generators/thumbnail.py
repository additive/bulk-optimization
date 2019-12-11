"""
Generates a compressed thumbnail for a video
"""

import sys
import ffmpeg

from generators.generator import Generator
from generators.jpg import JPG


class Thumbnail(Generator):
    async def run(self):
        self.start("Starting generator...")

        output = self.rename_extension(self.output_file, "jpg")
        output = self.rename_file(output, output.stem + "-thumb")
        if output.exists() and self.skip_existing:
            self.warn("Already exists, skipping...")
            return output

        try:
            (
                ffmpeg.input(self.input_file)
                .output(
                    filename=output,
                    vframes=1,
                    **{"hide_banner": None, "stats": None, "loglevel": "quiet"}
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            print(str(e.stderr, "utf-8"), file=sys.stderr)
            sys.exit(1)

        self.done()

        generator = JPG(self.group_name, self.group_label, output, output, False)
        output = await generator.run()

        return output

"""
Compresses a GIF
"""

from pygifsicle import gifsicle

from generators.generator import Generator


class GIF(Generator):
    async def run(self):
        self.start("Starting compression...")

        output = self.rename_extension(self.output_file, "gif")
        output.touch()  # create an empty file

        gifsicle(
            str(self.input_file),
            optimize=True,
            colors=100,
            destination=str(self.output_file),
            options=["--loopcount=forever", "-O3", "--lossy=30"],
        )

        self.done()
        return output

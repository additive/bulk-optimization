"""
Convert a image file to web save PNG
"""

from PIL import Image

from generators.generator import Generator


class PNG(Generator):
    async def run(self):
        self.start("(PNG )Starting compression...")

        output = self.rename_extension(self.output_file, "png")
        output.touch()  # create an empty file

        with Image.open(self.input_file) as img:
            img.thumbnail((1600, 900), Image.LANCZOS)
            img.compression_quality = 85
            img.type = "optimize"
            img.save(str(output), "PNG")
            img.close()

        self.done()
        return output

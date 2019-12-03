"""
Convert a image file to web save WEBP
"""

from PIL import Image

from generators.generator import Generator


class WEBP(Generator):
    async def run(self):
        self.start("Starting compression...")

        output = self.rename_extension(self.output_file, "webp")
        output.touch()  # create an empty file

        with Image.open(self.input_file) as img:
            img.convert("RGB")
            img.thumbnail((1600, 900), Image.LANCZOS)
            img.compression_quality = 85
            img.type = "optimize"
            img.save(str(output), "WEBP")
            img.close()

        self.done()
        return output

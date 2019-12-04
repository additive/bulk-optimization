"""
Convert a image file to web save PNG
"""

from PIL import Image

from generators.generator import Generator


class PNG(Generator):
    async def run(self):
        self.start("Starting compression...")

        output = self.rename_extension(self.output_file, "png")
        if output.exists() and self.skip_existing:
            self.warn("Already exists, skipping...")
            return output

        with Image.open(self.input_file) as img:
            img = img.convert("RGBA")
            img.thumbnail((1920, 1080), Image.LANCZOS)
            img.save(str(output), "PNG", compress_level=6, optimize=True)
            img.close()

        self.done()
        return output

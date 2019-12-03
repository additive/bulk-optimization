"""
Convert a image file to web save JPG
"""

from PIL import Image

from generators.generator import Generator


class JPG(Generator):
    async def run(self):
        self.start("Starting compression...")

        output = self.rename_extension(self.output_file, "jpg")
        output.touch()  # create an empty file

        with Image.open(self.input_file) as img:
            if img.mode in ("RGBA", "LA"):
                background = Image.new(img.mode[:-1], img.size, "#ffffff")
                background.paste(img, img.split()[-1])
                img = background
            else:
                img.convert("RGB")
            img.thumbnail((1600, 900), Image.LANCZOS)
            img.compression = "jpeg2000"
            img.compression_quality = 85
            img.type = "optimize"
            img.save(str(output), "JPEG")
            img.close()

        self.done()
        return output

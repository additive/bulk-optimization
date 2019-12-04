"""
Convert a image file to web save JPG
"""

from PIL import Image

from generators.generator import Generator


class JPG(Generator):
    async def run(self):
        self.start("Starting compression...")

        output = self.rename_extension(self.output_file, "jpg")
        if output.exists() and self.skip_existing:
            self.warn("Already exists, skipping...")
            return output

        with Image.open(self.input_file) as img:
            if img.mode in ("RGBA", "LA"):
                background = Image.new(img.mode[:-1], img.size, "#ffffff")
                background.paste(img, img.split()[-1])
                img = background
            img = img.convert("RGB")
            img.thumbnail((1920, 1080), Image.LANCZOS)
            img.save(
                str(output),
                "JPEG",
                jfif_unit=1,
                quality=85,
                optimize=True,
                progressive=True,
            )
            img.close()

        self.done()
        return output

"""
Convert a image file to web save WEBP
"""

from PIL import Image

from generators.generator import Generator


class WEBP(Generator):
    async def run(self):
        self.start("Starting compression...")

        output = self.rename_extension(self.output_file, "webp")
        if output.exists() and self.skip_existing:
            self.warn("Already exists, skipping...")
            return output

        with Image.open(self.input_file) as img:
            if img.mode in ("RGBA", "LA"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            img.thumbnail((1920, 1080), Image.LANCZOS)
            img.save(str(output), "WEBP", lossless=True, quality=85, method=2)
            img.close()

        self.done()
        return output

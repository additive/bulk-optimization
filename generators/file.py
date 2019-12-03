"""
Just moves files
"""

import sys

from shutil import copyfile

from generators.generator import Generator


class File(Generator):
    async def run(self):
        self.start("Moving file...")

        if self.output_file.exists():
            self.info("Already exists, skipping...")
            return self.output_file

        try:
            copyfile(self.input_file, self.output_file)
        except IOError as e:
            self.error("Unable to copy file. %s" % e)
        except:
            self.error("Unexpected error:", sys.exc_info())

        self.done()
        return self.output_file

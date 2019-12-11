"""
Base generator class
"""

from pathlib import Path
from sty import fg

from utils.display import Write, Box


class Generator:
    group_name = "generator"
    group_type = None
    group_label = None
    type_label = None

    input_file = None
    output_file = None
    skip_existing = True

    def __init__(self, group_name, group_type, input_file, output_file, skip_existing):
        self.group_name = group_name
        self.group_type = group_type
        self.group_label = Box.new(fg.li_black, group_name)
        self.type_label = " " + Box.new(fg.li_black, group_type) if group_type else ""

        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.skip_existing = skip_existing

    def start(self, *text):
        Write.next(self.group_label + self.type_label, *text)

    def info(self, *text):
        Write.info(self.group_label + self.type_label, *text)

    def error(self, *text):
        Write.error(self.group_label + self.type_label, *text)

    def warn(self, *text):
        Write.warn(self.group_label + self.type_label, *text)

    def done(self):
        Write.done(self.group_label + self.type_label, "Task successful!")

    def rename_extension(self, file_path, new_ext_name):
        return file_path.with_suffix("." + new_ext_name)

    def rename_file(self, file_path, new_file_name):
        return Path(
            str(file_path).replace(file_path.name, new_file_name) + file_path.suffix
        )

    def rename_folder(self, file_path, new_file_name):
        return Path(str(file_path).replace(file_path.name, new_file_name))

    async def run(self):
        Write.text("Input: {}".format(self.input_file))
        Write.text("Output: {}".format(self.output_file))
        return False

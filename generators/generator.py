"""
Base generator class
"""

from pathlib import Path
from sty import fg

from utils.display import Write, Box


class Generator:
    group = None
    type = None
    input_file = None
    output_file = None

    def __init__(self, group, type, input_file, output_file):
        self.group = group
        self.type = type
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)

    def start(self, *text):
        group_label = Box.new(fg.li_black, self.group)
        type_label = " " + Box.new(fg.li_black, self.type) if self.type else ""
        Write.next(
            group_label + type_label, *text,
        )

    def info(self, *text):
        group_label = Box.new(fg.li_black, self.group)
        type_label = " " + Box.new(fg.li_black, self.type) if self.type else ""
        Write.info(
            group_label + type_label, *text,
        )

    def error(self, *text):
        group_label = Box.new(fg.li_black, self.group)
        type_label = " " + Box.new(fg.li_black, self.type) if self.type else ""
        Write.fail(
            group_label + type_label, *text,
        )

    def done(self):
        group_label = Box.new(fg.li_black, self.group)
        type_label = " " + Box.new(fg.li_black, self.type) if self.type else ""
        Write.done(group_label + type_label, "Compression/conversion successful!")

    def rename_extension(self, file_path, new_ext_name):
        return Path(str(file_path).replace(file_path.suffix, "." + new_ext_name))

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

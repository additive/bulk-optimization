from sty import fg  # https://sty.mewo.dev/_images/charts.png

from utils.common import convert_bytes


def display_file_info(group, type, file_path):
    name = file_path.name
    size = convert_bytes(file_path.stat().st_size)
    group_label = Box.new(fg.li_black, group)
    type_label = " " + Box.new(fg.li_black, type) if type else ""
    Write.info(
        group_label + type_label, "Filename: {}".format(name),
    )
    Write.info(
        group_label + type_label, "Filesize: {}".format(size),
    )


class Box:
    @staticmethod
    def new(color, text):
        return "[" + color + str(text) + fg.rs + "]"


class Write:
    @staticmethod
    def text(*text):
        print(*text)

    @staticmethod
    def line():
        print()  # simple line break

    @staticmethod
    def info(*message):
        print(Box.new(fg.blue, "INFO"), *message)

    @staticmethod
    def next(*message):
        print(Box.new(fg.li_magenta, "NEXT"), *message)

    @staticmethod
    def warn(*message):
        print(Box.new(fg.yellow, "INFO"), *message)

    @staticmethod
    def error(*message):
        print(Box.new(fg.red, "FAIL"), *message)

    @staticmethod
    def done(*message):
        print(Box.new(fg.green, "DONE"), *message)

    @staticmethod
    def black(*text):
        print(fg.black, *text, fg.rs, sep="")

    @staticmethod
    def red(*text):
        print(fg.red, *text, fg.rs, sep="")

    @staticmethod
    def green(*text):
        print(fg.green, *text, fg.rs, sep="")

    @staticmethod
    def yellow(*text):
        print(fg.yellow, *text, fg.rs, sep="")

    @staticmethod
    def blue(*text):
        print(fg.blue, *text, fg.rs, sep="")

    @staticmethod
    def magenta(*text):
        print(fg.magenta, *text, fg.rs, sep="")

    @staticmethod
    def cyan(*text):
        print(fg.cyan, *text, fg.rs, sep="")

    @staticmethod
    def gray(*text):
        print(fg.li_black, *text, fg.rs, sep="")

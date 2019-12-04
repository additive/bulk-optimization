"""
Generates video thumbnails (VTT)
"""

import random
import shutil
import math
import tempfile
import datetime

from moviepy.editor import VideoFileClip
from PIL import Image
from click import progressbar
from pathlib import Path

from generators.generator import Generator


class VTT(Generator):
    async def run(self):
        self.start("Starting generator...")

        output = self.rename_extension(self.output_file, "jpg")
        output = self.rename_file(output, output.stem + "-vtt")
        if output.exists() and self.skip_existing:
            self.warn("Already exists, skipping...")
            return output

        self.size = (160, 90)
        self.columns = 7
        self.interval = "auto"

        videoFileClip = VideoFileClip(str(self.input_file))
        tmp, prefix = self.get_output_prefix()

        if self.interval == "auto":
            self.interval = self.calculate_interval(videoFileClip.duration)
        else:
            self.interval = int(self.interval)

        self.generate_frames(videoFileClip, self.interval, prefix, self.size)

        vtt_file = self.generate_sprite_from_frames(tmp, self.columns, self.size, output)

        shutil.rmtree(tmp, ignore_errors=True)

        self.done()
        return vtt_file

    def generate_frames(self, videoFileClip, interval, outputPrefix, size):
        self.info("Extracting", int(videoFileClip.duration / interval), "frames")

        frameCount = 0

        with progressbar(range(0, int(videoFileClip.duration), interval)) as items:
            pre_time = datetime.datetime(1, 1, 1, 0, 0, 0)
            datetime.time(0, 0, 0, 0)
            for i in items:
                filepath = self.extract_frame(
                    videoFileClip, i, outputPrefix, size, frameCount
                )

                now_time = pre_time + datetime.timedelta(seconds=interval)
                self.save_vtt_part(filepath, pre_time, now_time)
                pre_time = now_time

                frameCount += 1

        self.info("Frames extracted.")

    def generate_sprite_from_frames(self, tmp, columns, size, output):
        framesMap = sorted(list(tmp.glob("*.jpg")))

        outputImg = output
        outputVTT = self.rename_extension(output, "vtt")

        masterWidth = size[0] * columns
        masterHeight = size[1] * int(math.ceil(float(len(framesMap)) / columns))

        line, column = 0, 0

        with open(outputVTT, "w") as vtt_file:
            vtt_file.write("WEBVTT\n\n")
        finalImage = Image.new(
            mode="RGB", size=(masterWidth, masterHeight), color=(0, 0, 0, 0)
        )
        finalImage.save(str(outputImg))

        index = 0
        for filename in framesMap:
            locationX = size[0] * column
            locationY = size[1] * line

            video_info = Path(filename)
            video_info = str(video_info).replace("".join(video_info.suffixes), ".txt")
            video_info = open(video_info).read().splitlines()

            self.add_vtt_entry(
                outputVTT, video_info, index, locationX, locationY, size[0], size[1],
            )

            with Image.open(filename) as image:
                finalImage.paste(image, (locationX, locationY))

            column += 1
            index += 1

            if column == columns:
                line += 1
                column = 0

        finalImage.save(outputImg)
        return outputVTT

    def save_vtt_part(self, filepath, pre_time, now_time):
        filepath = Path(filepath)
        filename = self.rename_extension(filepath, "txt")
        with open(filename, "w") as txt_file:
            line_pre_time = pre_time.strftime("%H:%M:%S.%f")[:-3] + "\n"
            line_now_time = now_time.strftime("%H:%M:%S.%f")[:-3]
            txt_file.writelines([line_pre_time, line_now_time])

    def extract_frame(self, videoFileClip, moment, outputPrefix, size, frameCount):
        output = str(outputPrefix) + ("%05d.jpg" % frameCount)
        videoFileClip.save_frame(output, t=int(moment))
        self.resize_frame(output, size)
        return output

    def resize_frame(self, filename, size):
        image = Image.open(filename)
        image = image.resize(size, Image.LANCZOS)
        image.save(filename)

    def calculate_interval(self, duration):
        if duration <= 300:
            return 1
        elif duration <= 1200:
            return 2
        elif duration <= 3600:
            return 5
        return 10

    def add_vtt_entry(self, output, info, index, x, y, w, h):
        filename = output.stem
        with open(output, "a") as vtt_file:
            line_frame = str(index + 1) + "\n"
            line_time = "{} --> {}".format(info[0], info[1]) + "\n"
            line_info = "{}.jpg#xywh={},{},{},{}".format(filename, x, y, w, h) + "\n"
            vtt_file.writelines([line_frame, line_time, line_info, "\n"])

    def get_output_prefix(self):
        tmp = Path(tempfile.mkdtemp())
        tmp.mkdir(parents=True, exist_ok=True)
        return tmp, tmp / ("%032x_" % random.getrandbits(128))

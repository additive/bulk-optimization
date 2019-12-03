# Bulk Optimization

Convert and optimize any file in a directory and their children's into web compatible
formats, fast.

Suggestions and optimizations are highly appreciated! This is in the very beginning and
should help companies produces web save content without the pain.

- [Usage](#usage)
- [What happens?](#what-happens)
  - [Video files](#video-files)
  - [Images... TODO](#images-todo)
  - [GIF... TODO](#gif-todo)
  - [Other files... TODO](#other-files-todo)
- [Development](#development)
- [Next](#next)
- [Reads](#reads)

## Usage

```
Bulk Optimization

Iterate over a directory and perform compression, resizing and
formatting for optimal web capabilities.

Options:
    input_path      Where to start searching                (optional)
    output_path     Where to copy the folder structure      (optional)

Usage:
    python3 main.py
    python3 main.py /some/dir
    python3 main.py /some/dir /goes/here
```

## What happens?

### Video files

Video files like `mov` or `mp4` will be converted and optimized. It will generate a few
more files:

- MP4: the common file format for the web
- WEBM: web format to reduce file size by keeping video quality (needs better finetuning)
- Thumb: a thumbnail from the first frame in the video
- VTT:
  - JPG: a sprite containing thumbnails from the video based on a value
  - VTT: a file where each sprite frame is listed so video players can make use of them

### Images... TODO

### GIF... TODO

### Other files... TODO

## Development

1. Create a virtual env with `virtualenv` and install all requirements
2. Run `python3 main.py /some/dir/to/test/with/many/files`

## Next

- [ ] Create single executable
- [ ] Create UI?
- [ ] Add options (the hole process for this should be replaced)
  - [ ] Override option to not skip existing files
  - [ ] No thumbnail generation
  - [ ] No JPEG/PNG only Webp
  - [ ] No mp4 only Webm
  - [ ] Compression ratio

## Reads

- https://auth0.com/blog/image-processing-in-python-with-pillow/

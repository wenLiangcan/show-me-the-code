#!/usr/bin/env python

import sys

from PIL import Image, ImageDraw, ImageFont

TTF = 'Ubuntu-L'


def square_crop(img):
    """
    Crop the max square in the centre.
    """
    width, height = img.size
    padding = abs(width - height) // 2

    # PIL.Image.Image.crop(box=(A, B, C, D))
    #
    # |·A·|
    # ----+-------------------------
    # |   |           |       | ·  ·
    # |   |           |       | ·  B
    # |   |           |       | ·  ·
    # |---|-----------+-------|-·---
    # |   |\\\\\\\\\\\|       | D
    # |   |\\\\\\\\\\\|       | ·
    # |   |\\\\\\\\\\\|       | ·
    # |---+-----------+-------+--
    # |   |           |       |
    # |---------------+-------|
    # |·······C·······|
    if width > height:
        box = (padding, 0, width-padding, height)
    else:
        box = (0, padding, width, height-padding)
    square = img.crop(box)
    return square


def get_font(font, size=10):
    try:
        return ImageFont.truetype(font=font, size=size)
    except:
        return ImageFont.load(font)


def draw_badge(image, number, fnt=None):
    """
    Draw litile red number on the upper-right corner of the image.
    """
    TRANS  = (255, 255, 255, 0)
    RED = (255, 0, 0, 255)

    base = image.convert('RGBA')
    txt = Image.new('RGBA', base.size, TRANS)

    font_size = min(*base.size) // 4
    if not fnt:
        fnt = TTF
    font = get_font(fnt, size=font_size)

    d = ImageDraw.Draw(txt)

    width, height = base.size
    x, y = (width-font_size*len(number)//1.6, height//font_size*2.5)

    d.text((x, y), number, font=font, fill=RED)

    output = Image.alpha_composite(base, txt)

    return output


def main():
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument('image',
                           help='path to the image file')
    argparser.add_argument('number',
                           type=int,
                           help='the number shows on the upper-right corner of the image')
    argparser.add_argument('-c', '--crop',
                           help='crop the image to square',
                           action='store_true')
    argparser.add_argument('-o', '--out',
                           type=str,
                           help='output filename')
    argparser.add_argument('-f', '--format',
                           type=str,
                           choices=['jpeg', 'png'],
                           help='set output image format')
    argparser.add_argument('--font',
                           type=str,
                           help='set font used for the badge number')
    args = argparser.parse_args()

    PRE = 'bdg_'  # prefix for the generated file's name

    with Image.open(args.image) as img:
        if args.crop:
            base = square_crop(img)
        else:
            base = img
        output = draw_badge(base, str(args.number), args.font)

        oldname = args.image.split('/')[-1]
        if args.format:
            fmt = args.format.upper()
            filename = PRE + oldname.split('.')[0] + '.' + args.format
        else:
            fmt = ''
            filename = PRE + oldname
        if args.out:
            filename = args.out

        output.save(filename, format=fmt)


if __name__ == '__main__':
    main()


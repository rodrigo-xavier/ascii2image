import argparse
import os
from decode_xterm256 import decode_xterm256
from PIL import Image, ImageDraw, ImageOps, ImageFont


ANCHOR = (0, 0)

def get_args():
    parser = argparse.ArgumentParser("ASCII to Image")
    parser.add_argument('ascii', type=str, help="Path of ASCIIs or ASCII file")
    parser.add_argument('-x', action='store_true', help="For Xterm-256 Input")
    parser.add_argument('-b', default=["255", "255", "255"], metavar='N', type=str, nargs=3, help="Put here the Background Color of your text ASCII. Default = (255,255,255)")
    parser.add_argument('-c', default=["0", "0", "0"], metavar='N', type=str, nargs=3, help="Put here the color of your text ASCII. Default = (0,0,0)")
    parser.add_argument('--font', default="Hack-BoldItalic", metavar='F', type=str, help="Choose a Font Type that you like from fonts.txt. Default = Hack-BoldItalic")
    parser.add_argument('--fsize', default=20, type=int, help="Choose the font size you need. Default = 20")
    args = parser.parse_args()
    return args

def str2tuple(arg):
    x, y, z = arg
    return (int(x), int(y), int(z))

def common_ascii(args):
    with open(args.ascii, 'r') as f:
        font = ImageFont.truetype("fonts/" + args.font + ".ttf", args.fsize)

        image1 = Image.new("RGB", ANCHOR, str2tuple(args.b))
        draw1 = ImageDraw.Draw(image1)
        x, y, width, height = draw1.multiline_textbbox(ANCHOR, f.read(), font=font)

        f.seek(0)

        image2 = Image.new("RGB", (width, height), str2tuple(args.b))
        draw2 = ImageDraw.Draw(image2)
        draw2.multiline_text(ANCHOR, f.read(), font=font, fill=str2tuple(args.c))

        image2.save(args.ascii + '.png', "PNG")

def xterm_ascii(args):
    with open(args.ascii, 'r') as f:
        font = ImageFont.truetype("fonts/" + args.font + ".ttf", args.fsize)

        image1 = Image.new("RGB", ANCHOR, str2tuple(args.b))
        draw1 = ImageDraw.Draw(image1)
        x, y, width, height = draw1.multiline_textbbox(ANCHOR, f.read(), font=font)

        # Gambiarra para diminuir o tamanho da imagem de forma proposital
        width = int((width*5.5)/100)

        f.seek(0)

        image2 = Image.new("RGB", (width, height), str2tuple(args.b))
        draw2 = ImageDraw.Draw(image2)


        # x, y = 0, 0
        for line in f.readlines():
            line = decode_xterm256(line)
            max_y = 0
            x = 0

            for i in line:
                draw2.text((x,y), i[0] ,font=font, fill=i[1])
                letter_x, letter_y = draw2.textsize(i[0], font=font)

                max_y = max(max_y, letter_y)

                x = x + letter_x
            y = y + max_y

        image2.save(args.ascii + '.png', "PNG")


if __name__ == '__main__':
    args = get_args()

    if os.path.isfile(args.ascii):
        if not args.x:
            common_ascii(args)
        else:
            xterm_ascii(args)
    else:
        for file in os.listdir(args.ascii):
            if not args.x:
                common_ascii(args)
            else:
                xterm_ascii(args)

import argparse
import os
from decode_xterm256 import decode_xterm256
from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageEnhance


ANCHOR = (0, 0)

def get_args():
    parser = argparse.ArgumentParser("ASCII to Image")
    parser.add_argument('ascii', type=str, help="Path of ASCIIs or ASCII file")
    parser.add_argument('-x', action='store_true', help="For Xterm-256 Input")
    parser.add_argument('-b', default=["10", "10", "10"], metavar='N', type=str, nargs=3, help="Put here the Background Color of your text ASCII. Range[0-255, 0-255, 0-255]. Default = (10,10,10)")
    parser.add_argument('-c', default=["255", "255", "255"], metavar='N', type=str, nargs=3, help="Put here the color of your text ASCII. Range[0-255, 0-255, 0-255]. Default = (255,255,255)")
    parser.add_argument('-r', default=["40", "1"], metavar='R', type=int, nargs=2, help="Reduce a percentual space between ASCIIs characters . Range[1-99]. Default = (30, 1)")
    parser.add_argument('--font', default="Hack-BoldItalic", metavar='F', type=str, help="Choose a Font Type that you like from fonts.txt. Default = Hack-BoldItalic")
    parser.add_argument('--bitwise_xor', default=0, metavar='BT', type=int, help="Hexadecimal Bitwise_xor. Default = 0")
    parser.add_argument('--fsize', default=30, type=int, help="Choose the font size you need. Default = 30")
    args = parser.parse_args()
    return args

def list2tuple(arg):
    return tuple(map(int, arg))

def common_ascii(args):
    with open(args.ascii, 'r') as f:
        font = ImageFont.truetype("fonts/" + args.font + ".ttf", args.fsize)

        image_measure = Image.new("RGB", ANCHOR, list2tuple(args.b))
        drawing_measure = ImageDraw.Draw(image_measure)
        x, y, width, height = drawing_measure.multiline_textbbox(ANCHOR, f.read(), font=font)

        f.seek(0)

        image = Image.new("RGB", (width, height), list2tuple(args.b))
        draw = ImageDraw.Draw(image)
        draw.multiline_text(ANCHOR, f.read(), font=font, fill=list2tuple(args.c))

        image.save(args.ascii + '.png', "PNG")

def xterm_ascii(args):
        text, color = decode_xterm256(args)

        font = ImageFont.truetype("fonts/" + args.font + ".ttf", args.fsize)

        image_measure = Image.new("P", ANCHOR, list2tuple(args.b))
        drawing_measure = ImageDraw.Draw(image_measure)
        ignore1, ignore2, width, height = drawing_measure.multiline_textbbox(ANCHOR, text, font=font)

        image = Image.new("P", (width, height), list2tuple(args.b))
        draw = ImageDraw.Draw(image)
        contrast = ImageEnhance.Contrast(image)
        color = ImageEnhance.Color(image)

        index, x, y = 0, 0, 0

        for character in text:
            if character != '\n':
                bitwise_xor = hex(color[index] ^ args.bitwise_xor)
                bitwise_xor = bitwise_xor.ljust(10, '0')
                bitwise_xor = '#' + bitwise_xor[2:10]
                
                draw.text((x,y), character ,font=font, fill=bitwise_xor)
                
                x += args.r[0]
                index += 1
            else:
                x = 0
                y += args.r[1]
        
        image = image.convert('RGB')
        image = contrast.enhance(1.5)
        image = color.enhance(2.0)
        image = image.convert('P')
        
        image.save(args.ascii + '.png', "PNG")

if __name__ == '__main__':
    args = get_args()

    args.r[0] = args.fsize - int((args.fsize * int(args.r[0]))/100)
    args.r[1] = args.fsize - int((args.fsize * int(args.r[1]))/100)

    if os.path.isfile(args.ascii):
        if not args.x:
            common_ascii(args)
        else:
            xterm_ascii(args)
    else:
        folder = args.ascii
        for file in os.listdir(args.ascii):
            args.ascii = folder + file
            if not file.endswith((".png", ".jpg")):
                print("Opening File: " + args.ascii)
                if not args.x:
                    common_ascii(args)
                else:
                    xterm_ascii(args)

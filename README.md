```
usage: ASCII to Image [-h] [-x] [-b N N N] [-c N N N] [--font F] [--bitwise BT] [--fsize FSIZE] ascii

positional arguments:
  ascii          Path of ASCIIs or ASCII file

optional arguments:
  -h, --help     show this help message and exit
  -x             For Xterm-256 Input
  -b N N N       Put here the Background Color of your text ASCII. Default = (10,10,10)
  -c N N N       Put here the color of your text ASCII. Default = (255,255,255)
  --font F       Choose a Font Type that you like from fonts.txt. Default = Hack-BoldItalic
  --bitwise BT   Hexadecimal Bitwise (Multiply colors). Default = 4
  --fsize FSIZE  Choose the font size you need. Default = 30
```
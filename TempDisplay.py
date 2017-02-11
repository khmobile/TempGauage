

import os
import sys
import base64

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
import time
from papirus import Papirus
from papirus import PapirusImage

user = os.getuid()
if user != 0:
    print ("Please run script as root")
    sys.exit()
    
WHITE = 1
BLACK = 0

FONT_FILE = '/home/pi/Downloads/Bariol-Regular&Italic/Desktop/Bariol_Regular.otf'
FONT_BOLD = '/home/pi/Downloads/Bariol-Regular&Italic/Desktop/Bariol_Regular.otf'
TIME_FONT = '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'


tempFont_SIZE = 70
descriptionFont_SIZE  = 25
timeFont_Size = 15

MAX_START = 0xffff

 
def main(argv):

    papirus = Papirus()
    papirus.clear()
    tempDisplay(papirus)
  
def tempDisplay(papirus):
   count = 0
   image = Image.new('1', papirus.size, WHITE)

   while (count < 60):
        width, height = image.size
        now = datetime.today()
        tempFont = ImageFont.truetype(FONT_FILE, tempFont_SIZE )
        descriptionFont = ImageFont.truetype(FONT_BOLD, descriptionFont_SIZE)
        timeFont = ImageFont.truetype(TIME_FONT , timeFont_Size)
        img = Image.open('/home/pi/Mariah/image/coldDisp.bmp', 'r')
        draw = ImageDraw.Draw(img)
      #  draw.text((0,0), '{h:02d}:{m:02d}:{s:02d}'.format(h=now.hour, m=now.minute, s=now.second), fill=BLACK, font=timeFont)
        draw.text((57,30), "88\xb0", font=tempFont)
        draw.text((125,0),"Water",font=descriptionFont)
        bw = img.convert("1", dither=Image.FLOYDSTEINBERG)
        papirus.display(bw)
        papirus.partial_update()
        count +=1
       
      

# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass

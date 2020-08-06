

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

FONT_FILE = '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'
TIME_FONT = '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'


tempFont_SIZE = 50
descriptionFont_SIZE  = 10
timeFont_Size = 15
GAIN =1
MAX_START = 0xffff
tempFont = ImageFont.truetype(FONT_FILE, tempFont_SIZE )
descriptionFont = ImageFont.truetype(FONT_BOLD, descriptionFont_SIZE)
timeFont = ImageFont.truetype(TIME_FONT , timeFont_Size)
   
 
def main(argv):

    papirus = Papirus()
    papirus.clear()
    tempDisplay(papirus)
  
def tempDisplay(papirus):
   count = 0
   previous_second = 0
   
   while (count < 60):
        now = datetime.today()
        time.sleep(0.5)

        loadImage(papirus, 50)
        if now.second < previous_second:
           papirus.update()    # full update every minute
            
        else:
            papirus.partial_update()
        previous_second = now.second

        count +=1

        print('| {0} | {1} '.format(now.second,previous_second))



def loadImage(papirus,temp):
       image = Image.new('1', papirus.size, WHITE) 
       width, height = image.size
       img = Image.open('/home/pi/TempGauage/image/coldDisp.bmp', 'r')
       draw = ImageDraw.Draw(img)
       draw.text((57,30), "{0}\xb0".format(temp), font=tempFont)
       draw.text((90,0),"Mode:",font=descriptionFont)
       draw.text((125,0),"cool",font=descriptionFont)
    
       bw = img.convert("1", dither=Image.FLOYDSTEINBERG)
       papirus.display(bw)

 
# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass

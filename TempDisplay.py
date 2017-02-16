

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
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

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
        temp = getTemp(0)    
        loadImage(papirus, temp)
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
       img = Image.open('/home/pi/Mariah/image/coldDisp.bmp', 'r')
       draw = ImageDraw.Draw(img)
       draw.text((57,30), "{0}\xb0".format(temp), font=tempFont)
       draw.text((125,0),"Air",font=descriptionFont)
       bw = img.convert("1", dither=Image.FLOYDSTEINBERG)
       papirus.display(bw)

def getTemp(channel):
        GAIN = 2
        adc.start_adc(0, gain=GAIN)
        value= adc.read_adc(channel, gain=GAIN)
        compTemp =0
        rawValue = adc.get_last_result()
        compTemp = rawValue >> 5
        value = compTemp & 0b00000000001
        convertedTemp = compTemp * .125 * 1.8 +32
        return int(convertedTemp)
 
# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass

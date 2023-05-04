from PIL import Image
import os
import argparse
import colorsys
from termcolor import cprint
from math import sqrt

outputPixelValues = ['.',':','*',"+","0","#"]

class Size():
    Fit = 1
    Default = 2
    Custom = 3

parser = argparse.ArgumentParser(description='Output an image into terminal. By default scales according to terminal width whilst preserving ratio.')
parser.add_argument('image', metavar='Img', type=str,
                    help='The input image to be printed to terminal')
parser.add_argument('-F',  action='store_true',
                    help='Make the image fit the terminal window')
parser.add_argument('-S', nargs = 2, type=int,
                    help='Scale the image to custom size (width, height)')
parser.add_argument('-C', action='store_true',
                    help='Try to output the image coloured')
parser.add_argument('-T', action='store_true',
                    help='Use custom thresholding. Better for images with a lot of similar colour')

def getPixelChar(value,thresholds=None):
    if (thresholds != None):
        for m in range(len(thresholds)):
            if (value <= thresholds[m]):
                return outputPixelValues[m]
            
    size = len(outputPixelValues)
    
    for p in range(size):
        if (255/(size-p) >= value):
            return(outputPixelValues[size-1-p])

def printPixelGrey(pixRelVal,thresholds):
    print(getPixelChar(pixRelVal,thresholds),end="")
            
def thresholdImage(array):

    values = {}
    
    for p in array:
        if (p in values):
            values[p] += 1
        else:
            values[p] = 1

    thresholds = []
    curSum = 0
    for v in dict(sorted(values.items())):
        curSum += values[v]
        if (curSum > len(img.getdata())/len(outputPixelValues)):
            curSum = 0
            thresholds.append(v)
    return thresholds


def printPixelColour(pixel):
    (h , s , v) = colorsys.rgb_to_hsv(pixel[0],pixel[1],pixel[2])
    
    char = getPixelChar(v)
    colour = "red"
    if (h <= 30/360):
        colour = "red"
    elif (h <= 70/360):
        colour = "yellow"
    elif (h <= 160/360):
        colour = "green"
    elif (h <=200/360):
        colour = "cyan"
    elif (h <= 280/360):
        colour = "blue"
    else:
        colour = "magenta"
    
    if (s <= 0.3):
        colour = "black"
    elif (s >= 0.8):
        colour = "white"
    cprint(char,colour,force_color=True,end="")

def printImage(img):
    (w , _) = os.get_terminal_size()
    wDif = w - img.width 
    if (wDif < 0):
        wDif = 0
    wDif //= 2

    thresholds = None
    if (args.T):
        thresholds = thresholdImage(sorted(list(img.getdata())))

    for i in range(img.height):
        for j in range(img.width+wDif):
            if (j < wDif):
                print(' ',end="")
            else:
                pixel = img.getpixel((j-wDif,i))
                if (args.C):
                    printPixelColour(pixel)
                else:
                    printPixelGrey(pixel,thresholds)
        print()

def resizeImg(type,img):
    (w,h) = os.get_terminal_size()
    ratio = img.height/img.width
    if (type == Size.Fit):
        img = img.resize((w,h))
    elif (type == Size.Default):
        img = img.resize((w,int(w*ratio)))
    elif (type == Size.Custom):
        img = img.resize(args.S)
    return img



args = parser.parse_args()

img = Image.open(args.image)

if (args.F):
    type = Size.Fit
elif(args.S != None):
    type = Size.Custom
else:
    type = Size.Default

if (type == Size.Custom and args.S[0] > os.get_terminal_size()[0]):
    print("Width is bigger than windows size! Don't want this to happen, trust me.")
else:
    
    img = resizeImg(type,img)
    grey = img.convert('L')
    if (args.C == False):
        img = grey
    printImage(img)


    
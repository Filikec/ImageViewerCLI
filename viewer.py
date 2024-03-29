#!/usr/bin/env python
from PIL import Image, ImageFilter
import os
import argparse
import colorsys
from termcolor import cprint
from math import sqrt

outputPixelValues = ['.',':','"','*',"x","X","#","$","@"]
# ['.',':','*',"x","X","#","$","@"]
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
parser.add_argument('--no-ascii', action='store_true',
                    help="Don't use ascii for colour and use coloured bg instead")
parser.add_argument('-E', action='store_true',
                    help='Draw edges from the image instead')


# gets the corresponding character to pixel value
# decides according to threshold values or 0-255 range
def getPixelChar(value,thresholds=None):
    if (thresholds != None):
        for m in range(len(thresholds)):
            if (value <= thresholds[m]):
                return outputPixelValues[m]
            
    size = len(outputPixelValues)
    
    for p in range(size):
        if (255/(size-p) >= value):
            return(outputPixelValues[p])

def printPixelGrey(pixel,thresholds):
    print(getPixelChar(pixel,thresholds),end="")

# separate pixel values into n bins with approx same size where n is the number of output chars            
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


def printPixelColour(pixel,thresholds):
    (h , s , v) = colorsys.rgb_to_hsv(pixel[0],pixel[1],pixel[2])
    
    char = getPixelChar(v,thresholds)
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
    
    if (s <= 0.05):
        colour = "black"
    elif (s >= 0.8):
        colour = "white"
    
    if (args.no_ascii):
        cprint(" ",colour,force_color=True,on_color="on_"+colour,end="")
    else:
        cprint(char,colour,force_color=True,end="")

def printImage(img):
    (w , _) = os.get_terminal_size()
    wDif = w - img.width 
    if (wDif < 0):
        wDif = 0
    wDif //= 2

    thresholds = None
    if (args.T):
        if (args.C == False):
            thresholds = thresholdImage(sorted(list(img.getdata())))
        else:
            array = []
            for p in img.getdata():
                (_ , _ , v) = colorsys.rgb_to_hsv(p[0],p[1],p[2])
                array.append(v)
            thresholds = thresholdImage(sorted(array))


    for i in range(img.height):
        for j in range(img.width+wDif):
            if (j < wDif):
                print(' ',end="")
            else:
                pixel = img.getpixel((j-wDif,i))
                if (args.C):
                    printPixelColour(pixel,thresholds)
                else:
                    printPixelGrey(pixel,thresholds)
        print()

def resizeImg(type,img):
    (w,h) = os.get_terminal_size()
    ratio = img.height/img.width
    if (type == Size.Fit):
        newW = int(h*2/ratio)
        if (newW > w):
            img = img.resize((w,int(ratio*w/2)))
        else:
            img = img.resize((newW,h))
    elif (type == Size.Default):
        img = img.resize((w,int(w*ratio/2)))
    elif (type == Size.Custom):
        img = img.resize(args.S)
    return img

args = parser.parse_args()

if (args.no_ascii and args.C == False):
        parser.error('Cannot use --no-ascii without -C flag.')
if (args.S and args.F):
        parser.error('Can only use either F or S')

originalImage = Image.open(args.image)
greyImage = originalImage.convert('L')

if (args.F):
    type = Size.Fit
elif(args.S != None):
    type = Size.Custom
else:
    type = Size.Default


img = resizeImg(type,originalImage)
if (args.C == False):
    img = resizeImg(type,greyImage)
if (args.E):
    img = resizeImg(type,greyImage).filter(ImageFilter.FIND_EDGES)
printImage(img)


    
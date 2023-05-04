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
def getPixelChar(value):
    size = len(outputPixelValues)
    for p in range(size):
        if (255/(size-p) >= value):
            return(outputPixelValues[size-1-p])

def printPixelGrey(pixRelVal):
    print(getPixelChar(pixRelVal),end="")
            

def printPixelColour(pixel):
    (_ , _ , v) = colorsys.rgb_to_hsv(pixel[0],pixel[1],pixel[2])
    colours = {"red" : [255,0,0], "green" : [0,255,0], "blue" : [0,0,255],"yellow": [255,255,0], "cyan" : [0,255,255],"magenta" : [255,0,255], "black" : [0,0,0], "white" : [255,255,255]}
    
    char = getPixelChar(v)
    
    bestC = "black"
    least = 16581375
    for colour in colours:
        x = pixel[0] - colours[colour][0]
        y = pixel[1] - colours[colour][1]
        z = pixel[2] - colours[colour][2]
        dist = sqrt(x*x+y*y+z*z)
        if (dist < least):
            least = dist
            bestC = colour

    cprint(char,bestC,force_color=True,end="")

def printImage(img):
    (w , _) = os.get_terminal_size()
    wDif = w - img.width 
    if (wDif < 0):
        wDif = 0
    wDif //= 2
    img = img.convert()
    for i in range(img.height):
        for j in range(img.width+wDif):
            if (j < wDif):
                print(' ',end="")
            else:
                pixel = img.getpixel((j-wDif,i))
                if (args.C):
                    printPixelColour(pixel)
                else:
                    printPixelGrey(pixel)
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


    
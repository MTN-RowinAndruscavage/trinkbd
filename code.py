"""CircuitPython Trinkey USB HID typewriter."""
import os, time, gc, random
import board, digitalio
from rainbowio import colorwheel
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

import button2

# Delay between keystrokes
delay = 0.02

files = os.listdir('texts')
files.sort()
filenum = 0
text = ''


def loadText(filename):
    global text
    text = ''
    gc.collect()
    with open('texts/%s' % filename, 'r') as f:
        text = f.readlines()
    f.close()
    gc.collect()

loadText(files[filenum])

activated = False
changed = 0
continuous = 0
errorRate = 0
i = 0

def activateButton(button):
    global activated
    activated = True

def selectButton(button):
    global changed
    changed = 1
    
def toggleContinuous(button):
    global continuous, errorRate
    # Toggle between output modes:
    # 0 = one line
    # 1 = continuous output of a file
    # 2 = continuous errors
    continuous = (continuous + 1) % 3
    if continuous == 2:
        errorRate = 10
    else: errorRate = 0
    print("continuous = %d" % continuous)

def nextFile(button):
    global filenum
    filenum = (filenum + 1) % len(files)
    print("Loading %s" % files[filenum])
    loadText(files[filenum])
    # typestuff(files[filenum])
    
btn1 = button2.Button2(board.BUTTON)
btn1.setClickHandler(activateButton)
btn1.setDoubleClickHandler(selectButton)
btn1.setTripleClickHandler(nextFile)
btn1.setLongClickHandler(toggleContinuous)

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

def rainbow(delay):
    for color_value in range(255):
        pixel[0] = colorwheel(color_value)
        time.sleep(delay)

def typestuff(text):
    for char in text:
        
        if errorRate:
            # Set a chance to mix it up a little
            if not random.randint(0, errorRate * 4):
                char = chr(random.randint(ord('A'), ord('Z')))
            
            if not random.randint(0, errorRate):
                char = char.lower()
            elif not random.randint(0, errorRate):
                char = char.upper()                
            
            if not random.randint(0, errorRate * 4):
                kbd.send(Keycode.BACKSPACE)

            if not random.randint(0, errorRate * 4):
                kbd.send(Keycode.SPACEBAR)

        try:
            layout.write(char)
        except:
            print("Invalid character encountered: %s" % char)
        k = layout.keycodes(char)
        if (ord(char) > ord('a')):
            pixel.brightness = 0.1
            pixel[0] = colorwheel((ord(char) - ord('a')) * 9)
        else:
            pixel.brightness = 0.8
            pixel[0] = colorwheel((ord(char) - ord('A')) * 9)
        if errorRate:
            # Add an extra random delay between 0 - 1 second
            # ^4 to skew it towards shorter times
            time.sleep(0.4 * (random.randint(0, errorRate) / errorRate) ** 4)
        else:
            time.sleep(delay)

        pixel.fill((0, 0, 0))
        btn1.loop()

while True:
    btn1.loop()
    if continuous or activated:
        pixel.fill((0, 0, 0))
        pixel.brightness = 0.2
        
        ## Type in bulk
        # layout.write(text)
        
        ## Type character by character
        i = i % len(text)
        typestuff(text[i].replace('\r', ''))
        
        activated = 0
    if continuous or changed:
        i = (i + 1) % len(text)
        changed = 0
        print("  Line: %d" % i)
    else:
        pixel.brightness = 0.05
        pixel.fill((226, 0, 116))
    time.sleep(0.1)

# trinkbd
CircuitPython ghost typer for the Adafruit Trinkey QT Py 2040

Should work on little dongles like:
https://www.adafruit.com/product/5056 
https://www.adafruit.com/product/4900

Push button; get USB HID keycodes
Load up a directory with text files and go to town.

Also blinks the neopixel to correspond to the ASCII keycodes.

USAGE:
======

This has several modes:

  - Single click BOOT: Print current line.
  - Double click BOOT: Select next line.
  - Triple click BOOT: Load next text file.
  - Long click BOOT: toggle continuous mode within a text file.
  - RST: resets me.
  - Hold down BOOT after releasing RST: USB drive mode - modify my code or edit files in "texts" directory.
  - Hold down BOOT while releasing RST: UF2 Firmware update mode (don't kill me!).


INSTALLATION:
=============

You will need to copy the following CircuitPython Libraries to your device's lib/ dir
https://circuitpython.org/libraries
(Tested with CircuitPython 7.3)

  - neopixel.mpy
  - adafruit_hid/


LIMITATIONS:
============

The entire text file is loaded into memory as an array of strings, so you'll probably run out of memory with large files.

It'll want to get to the end of a line before responding to button presses.

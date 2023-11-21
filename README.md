# trinkbd
CircuitPython ghost typer for CircuitPython

One-button keyboard that automatically types stuff from onboard storage.  Push button; get USB HID keycodes.

Some possible use cases: 
  * Paste text into devices 
  * Automate repetitive tasks, like downloading and running a script that automates more reptitive tasks
  * Use it to enter long obnoxious passwords
  * Leave it connected to a computer and let it type away to spook people out, or to prevent the screensaver from kicking in.

Also blinks the neopixel to correspond to the ASCII keycodes.

Should work on little dongles like:

  * [Adafruit Trinkey QT2040](https://www.adafruit.com/product/5056) 
  * [Adafruit QT Py RP2040](https://www.adafruit.com/product/4900)


USAGE:
======

This has several modes:

  - Single click BOOT: Print current line.
  - Double click BOOT: Select next line.
  - Triple click BOOT: Load next text file.
  - Long click BOOT: toggle continuous mode within a text file.
  - RST: resets me.
  - Hold down BOOT after releasing RST: USB drive mode - modify my code or edit files in "texts/" directory.
  - Hold down BOOT while releasing RST: UF2 Firmware update mode.


INSTALLATION:
=============

You will need to copy the following CircuitPython Libraries to your device's lib/ dir
https://circuitpython.org/libraries
(Tested with CircuitPython 7.3 and 8.2)

  - neopixel.mpy
  - adafruit_hid/

Load up the texts/ directory with text files and go to town.

LIMITATIONS:
============

The entire text file is loaded into memory as an array of strings, so you'll probably run out of memory with large files.

It'll want to get to the end of a line before responding to button presses.


FUTURE:
=======

* Add keycap support which will allow CTRL, ALT, WIN key events so you can use it to Win-r and launch apps.  This would be useful for e.g. bootstrapping physical machines with dependencies to the point where ansible or some other kind of automation can take over.

* Add pauses, speed control

* Add some kind of random / catlike / AI/ML text generation modes

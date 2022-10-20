# trinkbd
CircuitPython ghost typer for the Adafruit Trinkey QT2040

Should work on litte dongles like:
https://www.adafruit.com/product/5056 
https://www.adafruit.com/product/4900

Push button; get USB HID keycodes
Load up a directory with text files and go to town.

Also blinks the neopixel to corresond to the ASCII keycodes.

This has several modes:

Single click BOOT: Print current line.
Double click BOOT: Select next line.
Triple click BOOT: Load next text file.
Long click BOOT: toggle continuous mode within a text file.
RST: resets me.
Hold down BOOT after releasing RST: USB drive mode - modify my code or edit files in "texts" directory.
Hold down BOOT while releasing RST: UF2 Firmware update mode (don't kill me!).

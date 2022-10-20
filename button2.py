# Based on Button2.cpp - Arduino Library to simplify working with buttons.
#   Created by Lennart Hennigs, October 28, 2017.
# ported to CircuitPython 7.3

import time
import board, digitalio

debounce_ms = const(50)
longclick_ms = const(250)
doubleclick_ms = const(400)

single_click = const(1)
double_click = const(2)
triple_click = const(3)
long_click   = const(4)


class Button2:
    def __init__(self, attachTo, debounceTimeout=debounce_ms, buttonMode=digitalio.Direction.INPUT, buttonPull=digitalio.Pull.UP):
        self.setDebounceTime(debounceTimeout)
        self.pinNum=attachTo
        self.pin=digitalio.DigitalInOut(attachTo)
        self.pin.direction = buttonMode
        self.pin.pull = buttonPull
        self.state = self.prev_state = True
        self.click_ms = 0
        self.down_ms = 0
        self.click_count = 0
        self.last_click_type = 0
        self.down_time_ms = 0
        self.pressed_triggered = False
        self.longclick_detected = False
        
        self.pressed_cb = None
        self.released_cb = None
        self.change_cb = None
        self.tap_cb = None
        self.click_cb = None
        self.long_cb = None
        self.double_cb = None
        self.triple_cb = None
        
    def setDebounceTime(self, ms):
        self.debounce_time_ms = ms
        
    def setChangedHandler(self, callback):
        self.pressed_cb = callback
    
    def setReleasedHandler(self, callback):
        self.released_cb = callback
        
    def setClickHandler(self, callback):
        self.click_cb = callback
        
    def setTapHandler(self, callback):
        self.tap_cb = callback
        
    def setLongClickHandler(self, callback):
        self.long_cb = callback
        
    def setDoubleClickHandler(self, callback):
        self.double_cb = callback
        
    def setTripleClickHandler(self, callback):
        self.triple_cb = callback
        
    def wasPressedFor(self):
        return self.down_time_ms
    
    def isPressed(self):
        return self.state == False
    
    def getNumberOfClicks(self):
        return self.click_count
    
    def getClickType(self):
        return self.last_click_type
    
    def loop(self):
        
        self.prev_state = self.state
        self.state = self.pin.value
        
        # is button pressed?
        if (self.prev_state == True) and (self.state == False):
            self.down_ms = int(time.monotonic() * 1000)
            self.pressed_triggered = False
            self.click_count += 1
            self.click_ms = self.down_ms
            
        # is the button released?
        elif (self.prev_state == False) and (self.state == True):
            self.down_time_ms = int(time.monotonic() * 1000) - self.down_ms
            # is it beyond debounce time?
            if (self.down_time_ms >= self.debounce_time_ms):
                # trigger release
                if (self.change_cb != None): self.change_cb(self)
                if (self.released_cb != None): self.released_cb(self)
                # trigger tap
                if (self.tap_cb != None): self.tap_cb(self)
                # was it a longclick? (preceeds single / double / triple clicks)
                if (self.down_time_ms >= longclick_ms):
                    self.longclick_detected = True
                    
        # trigger pressed event (after debounce has passed)
        elif (self.state == False) and not self.pressed_triggered and (int(time.monotonic() * 1000) - self.down_ms >= self.debounce_time_ms):
            if (self.change_cb != None): self.change_cb(self)
            if (self.pressed_cb != None): self.pressed_cb(self)
            self.pressed_triggered = True
            
        # is the button pressed and the time has passed for multiple clicks?
        elif (self.state == True) and int(time.monotonic() * 1000) - self.click_ms > doubleclick_ms:
            # was there a longclick?
            if (self.longclick_detected):
                # was it part of a combination?
                if (self.click_count == 1):
                    self.last_click_type = long_click
                    if (self.long_cb != None): self.long_cb(self)
                self.longclick_detected = False
            # determine the number of single clicks
            elif (self.click_count > 0):
                if self.click_count == 1:
                    self.last_click_type = single_click
                    if (self.click_cb != None): self.click_cb(self)
                elif self.click_count == 2:
                    self.last_click_type = double_click
                    if (self.double_cb != None): self.double_cb(self)
                elif self.click_count == 3:
                    self.last_click_type = triple_click
                    if (self.triple_cb != None): self.triple_cb(self)
            self.click_count = 0
            self.click_ms = 0
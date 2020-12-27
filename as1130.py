#!/usr/bin/python2

import smbus
import time
import sys

class AS1130(object):
    """ class for easier use of AS1130 chips on an I2C bus """
    # Ram section selection
    REG_SELECTION =             0xFD
    REG_FRAME_0 =               0x01
    REG_PWM_0 =                 0x40
    REG_CONTROL =               0xC0

    # Control register
    REG_PICTURE =               0x00
    REG_MOVIE =                 0x01
    REG_MOVIE_MODE =            0x02
    REG_FRAME_TIME_SCROLL =     0x03
    REG_DISPLAY_OPTION =        0x04
    REG_CURRENT_SOURCE =        0x05
    REG_CONFIG =                0x06
    REG_INTERRUPT_MASK =        0x07
    REG_INTERRUPT_FRAME =       0x08
    REG_SHUTDOWN =              0x09
    REG_I2C_MONITOUR =          0x0A
    REG_INTERRUPT_STATUS =      0x0E
    REG_STATUS =                0x0F

    WIDTH = 11
    HEIGHT = 10

    ADDRESS_MAP = [
        [(0x01, 0x02), (0x01, 0x01), (0x00, 0x80), (0x00, 0x40), (0x00, 0x20), (0x00, 0x10), (0x00, 0x08), (0x00, 0x04), (0x00, 0x02), (0x00, 0x01), (0x02, 0x01)],
        [(0x03, 0x02), (0x03, 0x01), (0x02, 0x80), (0x02, 0x40), (0x02, 0x20), (0x02, 0x10), (0x02, 0x08), (0x02, 0x04), (0x02, 0x02), (0x04, 0x02), (0x04, 0x01)],
        [(0x05, 0x02), (0x05, 0x01), (0x04, 0x80), (0x04, 0x40), (0x04, 0x20), (0x04, 0x10), (0x04, 0x08), (0x04, 0x04), (0x06, 0x04), (0x06, 0x02), (0x06, 0x01)],
        [(0x07, 0x02), (0x07, 0x01), (0x06, 0x80), (0x06, 0x40), (0x06, 0x20), (0x06, 0x10), (0x06, 0x08), (0x08, 0x08), (0x08, 0x04), (0x08, 0x02), (0x08, 0x01)],
        [(0x09, 0x02), (0x09, 0x01), (0x08, 0x80), (0x08, 0x40), (0x08, 0x20), (0x08, 0x10), (0x0A, 0x10), (0x0A, 0x08), (0x0A, 0x04), (0x0A, 0x02), (0x0A, 0x01)],
        [(0x0B, 0x02), (0x0B, 0x01), (0x0A, 0x80), (0x0A, 0x40), (0x0A, 0x20), (0x0C, 0x20), (0x0C, 0x10), (0x0C, 0x08), (0x0C, 0x04), (0x0C, 0x02), (0x0C, 0x01)],
        [(0x0D, 0x02), (0x0D, 0x01), (0x0C, 0x80), (0x0C, 0x40), (0x0E, 0x40), (0x0E, 0x20), (0x0E, 0x10), (0x0E, 0x08), (0x0E, 0x04), (0x0E, 0x02), (0x0E, 0x01)],
        [(0x0F, 0x02), (0x0F, 0x01), (0x0E, 0x80), (0x10, 0x80), (0x10, 0x40), (0x10, 0x20), (0x10, 0x10), (0x10, 0x08), (0x10, 0x04), (0x10, 0x02), (0x10, 0x01)],
        [(0x11, 0x02), (0x11, 0x01), (0x13, 0x01), (0x12, 0x80), (0x12, 0x40), (0x12, 0x20), (0x12, 0x10), (0x12, 0x08), (0x12, 0x04), (0x12, 0x02), (0x12, 0x01)],
        [(0x13, 0x02), (0x15, 0x02), (0x15, 0x01), (0x14, 0x80), (0x14, 0x40), (0x14, 0x20), (0x14, 0x10), (0x14, 0x08), (0x14, 0x04), (0x14, 0x02), (0x14, 0x01)],
    ]



    def __init__(self, bus, address):
        """ Initialise the chip """
        self.BUS = smbus.SMBus(bus)
        self.ADDRESS = address
        time.sleep(0.01)
        self.initRAMConfig()
        self.initControlRegister()
        # To light up the LEDs set the shdn bit to 1 for normal operation mode (see Table 23 on page 26).
        self.selectRamSection(AS1130.REG_CONTROL)
        self.writeByte(AS1130.REG_SHUTDOWN, 0x03)

    def initRAMConfig(self):
        """ Define RAM Configuration; bit mem_conf in the AS1130 Config Register (see Table 20 on page 25)
            -On/Off Frames
            -Blink & PWM Sets
            -Dot Correction, if specified
        """
        # Define RAM config
        self.selectRamSection(AS1130.REG_CONTROL)
        self.writeByte(AS1130.REG_CONFIG, 0x01)
        # Clear frame
        self.clear()

        # Define blink & PWM Sets
        self._setBlinkAll(0x00)
        self._setPwmAll(0xFF)

    def initControlRegister(self):
        """ Define Control Register (see Table 13 on page 20)
            -Current Source
            -Display picture / play movie
        """
        self.selectRamSection(AS1130.REG_CONTROL)
        # Current source
        self.writeByte(AS1130.REG_CURRENT_SOURCE, 0xFF)
        # Display picture
        self.writeByte(AS1130.REG_PICTURE, int("01000000", 2))
        # Set scan limit
        self.writeByte(AS1130.REG_DISPLAY_OPTION, int("00101010", 2))

    def setLed(self, x, y, value=True):
        """ Set (or clear) the LED at the coordinates x, y """
        assert(0 <= x < self.WIDTH)
        assert(0 <= y < self.HEIGHT)
        self.selectRamSection(AS1130.REG_FRAME_0)
        self._setBitField(AS1130.ADDRESS_MAP[y][x][0], AS1130.ADDRESS_MAP[y][x][1], value)


    def clear(self):
        self.selectRamSection(AS1130.REG_FRAME_0)
        for i in range(0xF):
            self.writeByte(2 * i, 0x00)
            self.writeByte(2 * i + 1, 0x00)

    def set(self):
        self.selectRamSection(AS1130.REG_FRAME_0)
        for i in range(0xF):
            self.writeByte(2 * i, 0xFF)
            self.writeByte(2 * i + 1, 0xFF)

    def fadeIn(self):
        for i in range(101):
            self._setPwmAll(0xFF * i / 100)
            time.sleep(0.0001)

    def fadeOut(self):
        for i in range(0, 101):
            self._setPwmAll(0xFF * (100 - i) /100)
            time.sleep(0.0001)

    def _setBitField(self, addr, bitField, value=True):
        self.selectRamSection(AS1130.REG_FRAME_0)
        data = self.readByte(addr)
        if value:
            data |= bitField
        else:
            data &= ~bitField
        self.writeByte(addr, data)

    def _setBlinkAll(self, value):
        self.selectRamSection(AS1130.REG_PWM_0)
        for i in range(0x0, 0x17 + 1):
            self.writeByte(i, value)

    def _setPwmAll(self, value):
        self.selectRamSection(AS1130.REG_PWM_0)
        for i in range(0x18, 0x9B + 1):
            self.writeByte(i, value)

    def selectRamSection(self, reg):
        """ Select the RAM section """
        self.writeByte(AS1130.REG_SELECTION, reg)

    def writeByte(self, reg, value):
        """ Write a byte to this chips address """
        self.BUS.write_byte_data(self.ADDRESS, reg, value)

    def readByte(self, reg):
        """ Read a byte from this chips address """
        return self.BUS.read_byte_data(self.ADDRESS, reg)

    def dump(self, reg):
        print "Dump of {:02x}:".format(reg)
        self.selectRamSection(reg)
        sys.stdout.write("{:4}".format(""))
        for i in range(0x0, 0xF + 1):
            sys.stdout.write("{:2x} ".format(i))
        print""
        for i in range(0x0, 0xF0 + 1, 0x10):
            sys.stdout.write("{:02x}: ".format(i))
            for j in range(0x0, 0xF + 1):
                sys.stdout.write("{:02x} ".format(self.readByte(i + j)))
            print ""
        print "\n"
    
    

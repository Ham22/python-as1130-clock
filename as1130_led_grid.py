import smbus
import time
import sys

from led_grid import LedGrid


class AS1130LedGrid(LedGrid):
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
        self._init_ram_config()
        self._init_control_register()
        # To light up the LEDs set the shdn bit to 1 for normal operation mode
        # (see Table 23 on page 26).
        self._select_ram_section(AS1130LedGrid.REG_CONTROL)
        self._write_byte(AS1130LedGrid.REG_SHUTDOWN, 0x03)

    def _init_ram_config(self):
        """ Define RAM Configuration; bit mem_conf in the AS1130 Config Register
         (see Table 20 on page 25)
            -On/Off Frames
            -Blink & PWM Sets
            -Dot Correction, if specified
        """
        # Define RAM config
        self._select_ram_section(AS1130LedGrid.REG_CONTROL)
        self._write_byte(AS1130LedGrid.REG_CONFIG, 0x01)
        # Clear frame
        self.clear()

        # Define blink & PWM Sets
        self._set_blink_all(0x00)
        self._set_pwm_all(0xFF)

    def _init_control_register(self):
        """ Define Control Register (see Table 13 on page 20)
            -Current Source
            -Display picture / play movie
        """
        self._select_ram_section(AS1130LedGrid.REG_CONTROL)
        # Current source
        self._write_byte(AS1130LedGrid.REG_CURRENT_SOURCE, 0xFF)
        # Display picture
        self._write_byte(AS1130LedGrid.REG_PICTURE, int("01000000", 2))
        # Set scan limit
        self._write_byte(AS1130LedGrid.REG_DISPLAY_OPTION, int("00101010", 2))

    def set_led(self, x, y, value=True):
        """ Set (or clear) the LED at the coordinates x, y """
        assert(0 <= x < self.WIDTH)
        assert(0 <= y < self.HEIGHT)
        self._select_ram_section(AS1130LedGrid.REG_FRAME_0)
        self._set_bit_field(AS1130LedGrid.ADDRESS_MAP[y][x][0],
                            AS1130LedGrid.ADDRESS_MAP[y][x][1], value)

    def clear(self):
        self._select_ram_section(AS1130LedGrid.REG_FRAME_0)
        for i in range(0xF):
            self._write_byte(2 * i, 0x00)
            self._write_byte(2 * i + 1, 0x00)

    def fade_in(self):
        for i in range(101):
            self._set_pwm_all(0xFF * i / 100)
            time.sleep(0.0001)

    def fade_out(self):
        for i in range(0, 101):
            self._set_pwm_all(0xFF * (100 - i) / 100)
            time.sleep(0.0001)

    def _set_bit_field(self, addr, bit_field, value=True):
        self._select_ram_section(AS1130LedGrid.REG_FRAME_0)
        data = self._read_byte(addr)
        if value:
            data |= bit_field
        else:
            data &= ~bit_field
        self._write_byte(addr, data)

    def _set_blink_all(self, value):
        self._select_ram_section(AS1130LedGrid.REG_PWM_0)
        for i in range(0x0, 0x17 + 1):
            self._write_byte(i, value)

    def _set_pwm_all(self, value):
        self._select_ram_section(AS1130LedGrid.REG_PWM_0)
        for i in range(0x18, 0x9B + 1):
            self._write_byte(i, value)

    def _select_ram_section(self, reg):
        """ Select the RAM section """
        self._write_byte(AS1130LedGrid.REG_SELECTION, reg)

    def _write_byte(self, reg, value):
        """ Write a byte to this chips address """
        self.BUS.write_byte_data(self.ADDRESS, reg, value)

    def _read_byte(self, reg):
        """ Read a byte from this chips address """
        return self.BUS.read_byte_data(self.ADDRESS, reg)

    def dump(self, reg):
        print("Dump of {:02x}:".format(reg))
        self._select_ram_section(reg)
        sys.stdout.write("{:4}".format(""))
        for i in range(0x0, 0xF + 1):
            sys.stdout.write("{:2x} ".format(i))
        print("")
        for i in range(0x0, 0xF0 + 1, 0x10):
            sys.stdout.write("{:02x}: ".format(i))
            for j in range(0x0, 0xF + 1):
                sys.stdout.write("{:02x} ".format(self._read_byte(i + j)))
            print("")
        print("\n")

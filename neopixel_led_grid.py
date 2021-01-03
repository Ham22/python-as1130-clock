import logging

import time

from led_grid import LedGrid


class NeoPixelLedGrid(LedGrid):
    # PIXEL_COUNT = 144
    WIDTH = 11
    HEIGHT = 10 + 1  # extra row is for the four corners
    MIN_BRIGHTNESS = 0
    MAX_BRIGHTNESS = 5
    LED_COLOUR = (255, 255, 255)
    LED_OFF = (0, 0, 0)
    ADDRESS_MAP = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11],
        [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
        [43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33],
        [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54],
        [65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55],
        [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76],
        [87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77],
        [88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98],
        [109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99],
        [110, 111, 112, 113, None, None, None, None, None, None, None],
    ]

    def __init__(self, colour=LED_COLOUR):
        # Only import if constructed to allow unittesting
        import neopixel
        import board
        led_count = self.WIDTH * self.HEIGHT
        self._pixels = neopixel.NeoPixel(board.D18,
                                         led_count,
                                         brightness=1,
                                         auto_write=False)
        self.colour = colour
        self.led_enable_buffer = [False] * led_count
        logging.info("Setup grid {}x{} with {} leds of colour {}".format(
            self.WIDTH, self.HEIGHT, led_count, self.colour
        ))

    def set_led(self, x, y, value=True):
        assert(0 <= x < self.WIDTH)
        assert(0 <= y < self.HEIGHT)
        self.led_enable_buffer[self.ADDRESS_MAP[y][x]] = value

    def clear(self):
        for i in range(len(self.led_enable_buffer)):
            self.led_enable_buffer[i] = False
        self._update_pixels(self.LED_COLOUR)

    def fade_out(self):
        for i in range(self.MAX_BRIGHTNESS, self.MIN_BRIGHTNESS-1, -1):
            self._update_pixels(self.colour, i)
            time.sleep(0.0001)

    def fade_in(self):
        for i in range(self.MIN_BRIGHTNESS, self.MAX_BRIGHTNESS+1):
            self._update_pixels(self.colour, i)
            time.sleep(0.0001)

    def _update_pixels(self, colour, brightness=MAX_BRIGHTNESS):
        if brightness == 100:
            adjusted_colour = colour
        elif brightness == 0:
            adjusted_colour = self.LED_OFF
        else:
            adjusted_colour = [value * brightness // 100 for value in colour]

        self._pixels[::] = [adjusted_colour if x else self.LED_OFF
                            for x in self.led_enable_buffer]
        self._pixels.show()

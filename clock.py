#!/usr/bin/python3

import datetime
import logging

import argparse
import time


class Clock:
    CONFIG = {
        "common": [
            [0, 0], [1, 0],
            [3, 0], [4, 0]
        ],
        "hours": {
            "0": [
                [5, 8], [6, 8], [7, 8], [8, 8], [9, 8], [10, 8]
            ],
            "1": [
                [0, 5], [1, 5], [2, 5]
            ],
            "2": [
                [8, 6], [9, 6], [10, 6]
            ],
            "3": [
                [6, 5], [7, 5], [8, 5], [9, 5], [10, 5]
            ],
            "4": [
                [0, 6], [1, 6], [2, 6], [3, 6]
            ],
            "5": [
                [4, 6], [5, 6], [6, 6], [7, 6]
            ],
            "6": [
                [3, 5], [4, 5], [5, 5]
            ],
            "7": [
                [0, 8], [1, 8], [2, 8], [3, 8], [4, 8]
            ],
            "8": [
                [0, 7], [1, 7], [2, 7], [3, 7], [4, 7]
            ],
            "9": [
                [7, 4], [8, 4], [9, 4], [10, 4]
            ],
            "10": [
                [0, 9], [1, 9], [2, 9]
            ],
            "11": [
                [5, 7], [6, 7], [7, 7], [8, 7], [9, 7], [10, 7]
            ]
        }, 
        "fiveminutes": {
            "0": [
                [5, 9], [6, 9], [7, 9], [8, 9], [9, 9], [10, 9]
            ],
            "5": [
                [6, 2], [7, 2], [8, 2], [9, 2],
                [0, 4], [1, 4], [2, 4], [3, 4]
            ],
            "10": [
                [5, 3], [6, 3], [7, 3],
                [0, 4], [1, 4], [2, 4], [3, 4]
            ],
            "15": [
                [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1],
                [0, 4], [1, 4], [2, 4], [3, 4]
            ],
            "20": [
                [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2],
                [0, 4], [1, 4], [2, 4], [3, 4]
            ],
            "25": [
                [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [9, 2],
                [0, 4], [1, 4], [2, 4], [3, 4]
            ],
            "30": [
                [0, 3], [1, 3], [2, 3], [3, 3],
                [0, 4], [1, 4], [2, 4], [3, 4]
            ],
            "35": [
                [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [9, 2],
                [9, 3], [10, 3]
            ],
            "40": [
                [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2],
                [9, 3], [10, 3]
            ],
            "45": [
                [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1],
                [9, 3], [10, 3]
            ],
            "50": [
                [5, 3], [6, 3], [7, 3],
                [9, 3], [10, 3]
            ],
            "55": [
                [6, 2], [7, 2], [8, 2], [9, 2],
                [9, 3], [10, 3]
            ]
        },
        "minutes": {
            "0": [],
            "1": [[0, 10]],
            "2": [[0, 10], [1, 10]],
            "3": [[0, 10], [1, 10], [2, 10]],
            "4": [[0, 10], [1, 10], [2, 10], [3, 10]]
        }
    }
    
    def __init__(self, grid, animations_on=True):
        self.grid = grid
        self.animations_on = animations_on
        self.minute = None

    def start(self):
        while True:
            t = datetime.datetime.now()
            self.update_time(t.hour, t.minute)
            time.sleep(5)

    def update_time(self, hour, minute):
        try:
            hour = hour + 1 if 55 < minute else hour
            minute = minute % 60
            next_hour = 30 < minute <= 55
            hour = hour + 1 if next_hour else hour
            hour = hour % 12
            logging.debug("It is {} {} {}".format(minute if not next_hour else 60 - minute, "past" if not next_hour else "to", hour))
            if self.minute != minute:
                self.minute = minute
                if self.animations_on:
                    self.grid.fade_out()
                self.grid.clear()
                list(map(lambda coord: self.grid.set_led(*coord),
                    self.CONFIG["common"] +
                    self.CONFIG["hours"][str(hour)] +
                    self.CONFIG["fiveminutes"][str(minute - (minute % 5))] +
                    self.CONFIG["minutes"][str(minute % 5)]
                    ))
                if self.animations_on:
                    self.grid.fade_in()
        except Exception as e:
            logging.exception(e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='Word clock.')
    parser.add_argument("--grid", default="neo", type=str,
                        choices=["neopixel", "as1130"],
                        help="choose grid hardware")
    args = parser.parse_args()
    if args.grid == "as1130":
        from as1130_led_grid import AS1130LedGrid
        clock = Clock(AS1130LedGrid(0, 0x30))
    else:
        from neopixel_led_grid import NeoPixelLedGrid
        clock = Clock(NeoPixelLedGrid())

    clock.start()

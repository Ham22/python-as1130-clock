# LED word clock
A personal project containing some basic code to drive an LED grid used to represent a clock face
that sits in my front room :D. Much like that seen on https://www.timeanddate.com/wordclock/.

This code has evolved over time and in its current form supports two types of LED grid:
* AS1130 - a dedicated IC, that utilises a charlieplexed grid of LEDs, controlled over i2c.
* NeoPixels - individually addressable RGB LEDs, that can be chained, controlled over one wire.

In both cases a simple python app is running on a raspberry pi 2 model B as a controller because
that is what I had lying around, but it should work on any hardware that supports the desired
interface.

## Dependencies
The control code is python 3.x based, the dependencies depend on the desired interface but they can
installed using `python3 -m pip install -r requirements.txt`.

## Configuring
The code is a bit hacky, and the config is quite specific to some hardware choices I have made
for example i2c addresses and physical LED locations so this config may need changing.

Some config can be done at runtime:
```
usage: clock.py [-h] [--grid {neo,as1130}]

Word clock.

optional arguments:
  -h, --help           show this help message and exit
  --grid {neopixel,as1130}
                        choose grid hardware
```

## Deploying
1. Check you have configured the code for your needs.
2. Run the deployment script `./scripts/deploy-to-target.sh <ip-of-pi>`

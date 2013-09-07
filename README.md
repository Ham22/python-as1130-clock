# LED clock python driver for AS1130

A personal project containing some very basic helper code to initialise an AS1130 and use it to
drive a charlieplexed LED array to use as a clock that sits in my front room :D. I use a raspberry
pi 2 Model B as a controller because it's what I had lying around but should work with anything.

## Dependencies
The control code is python 2.x based and should only need the following dependency:
* pysmbus

## Install
1. Check what i2c address your AS1130 is using, mine was `0x30` on the first i2c bus on the pi hence
the following init code:

```
self.chip = AS1130(0, 0x30)
```

2. Copy over the code to the controller e.g. under `/home/pi`
3. Install `sysvinit-clock.sh` to `/etc/init.d/clock.sh` on the controller and do any local config
required. (Don't forget to symlink it under `/etc/rc5.d/` for it to run).

## TODO
* Sort out the corners to represent minutes
* Generalise the config

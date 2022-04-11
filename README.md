## references

Terminal app and utils for midi event routing, mapping and scripting.
Comes with nanokontrol2 multichannel mappings.

1. make sure you have a [virtual midi cable](https://www.tobias-erichsen.de/software/loopmidi.html) defaults to  named *"cable"* or *"cableXXX"`*
2. connect nanokontrol editor with factory settings
3. `python midirouter.py`

The virtual midi cable will now work as nanoKontrol2 with additional 16 channels cycle and select.

```
# nanokontrol2 mappings
CYCLE             # hold to show active channel LED
TRACK >           # cycle midi channel forward
TRACK <           # cycle midi channel backward
CYCLE + MUTE1-8   # select midi channel 1-8
CYCLE + ARM1-8    # select midi channel 9-16
```


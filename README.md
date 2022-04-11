## references

Terminal app and utils for midi event routing, mapping and scripting.
Comes with nanokontrol2 mappings for channel 1-16 select.

1. add a [virtual midi instrument](https://www.tobias-erichsen.de/software/loopmidi.html) named to *"cable"* or *"cableXXX"`*
2. connect nanokontrol editor with factory settings
3. `python midirouter.py`

The virtual midi "cable" will now work as nanoKontrol2 with 16 midi channels.

```
# nanokontrol2 mappings
CYCLE             # hold to show active channel LED
TRACK >           # cycle midi channel forward
TRACK <           # cycle midi channel backward
CYCLE + MUTE1-8   # select midi channel 1-8
CYCLE + ARM1-8    # select midi channel 9-16
```


import time
from rtmidi import midiutil

midiin = midiutil.open_midiinput('nano')
midiout = midiutil.open_midioutput('nano')
cableout = midiutil.open_midioutput('cable')
print(midiin)
print(cableout)

KEY_CYCLE = 46
KEY_PREV = 58
KEY_NEXT = 59
KEYS_ARM = [64, 65, 66, 67, 68, 69, 70, 71]
channel = 0
isCycling = False

def onmidi(event, data=None):
    global channel, isCycling
    message, deltatime = event
    status, note, velocity = message
    iscc = message[0] == 176
    isnote_on = velocity == 127
    if iscc:
        if message[1] == KEY_CYCLE:
            isCycling = isnote_on
            paint_leds(isnote_on)
        elif message[1] == KEY_PREV:
            if isnote_on:
                channel = (channel - 1) % 8
            paint_leds(isnote_on)
        elif iscc and message[1] == KEY_NEXT:
            if isnote_on:
                channel = (channel + 1) % 8
            paint_leds(isnote_on)
        elif iscc and note in KEYS_ARM and isnote_on and isCycling:
            # select channel pressing cycle+arm[1,8]
            channel = KEYS_ARM.index(note)
            paint_leds(True)

    send_channel_message(status, note, velocity, channel)
midiin[0].set_callback(onmidi)

def paint_leds(paint_channel=True):
    for key in KEYS_ARM:
        send_channel_message(176, key, 0, 0, midiout[0]) # clear leds
    if paint_channel:
        send_channel_message(176, KEYS_ARM[0] + channel, 127, 0, midiout[0])

def send_channel_message(status, data1=None, data2=None, ch=channel, out=cableout[0]):
    """Send a MIDI channel mode message."""
    msg = [(status & 0xF0) | (ch & 0xF)]
    if data1 is not None:
        msg.append(data1 & 0x7F)
        if data2 is not None:
            msg.append(data2 & 0x7F)
    out.send_message(msg)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass;
finally:
    print('closing...')
    midiin[0].close_port()
    midiout[0].close_port()
    cableout[0].close_port()
    del midiin
    del midiout

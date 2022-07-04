import time
from rtmidi import midiutil

midiin = midiutil.open_midiinput('maschine')
midiout = midiutil.open_midioutput('maschine')
print(midiin)
print(midiout)

CHANNEL = 0
KEYS_GROUPS = [ 60, 61, 62, 43, 44, 42, 41, 45 ] # transport buttons
KEYS_PADS = [
    48, 49, 50, 51,
    52, 53, 54, 55, # 0-7 channels mute buttons
    64, 65, 66, 67, # 8-15 channels arm buttons
    64, 65, 66, 67  # 8-15 channels arm buttons
]

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
                channel = (channel - 1) % 16
            paint_leds(isnote_on)
        elif iscc and message[1] == KEY_NEXT:
            if isnote_on:
                channel = (channel + 1) % 16
            paint_leds(isnote_on)
        elif iscc and note in KEYS_ARM and isnote_on and isCycling:
            # select channel pressing cycle+arm[1,16]
            channel = KEYS_ARM.index(note)
            paint_leds(True)
        elif iscc and note in KEYS_ARM and isnote_on and isCycling:
            # select channel pressing cycle+arm[1,16]
            channel = KEYS_ARM.index(note)
            paint_leds(True)

    # pipe messages with the modified channel# virtual midicables
    send_channel_message(status, note, velocity, channel)
midiin[0].set_callback(onmidi)

def paint_leds(paint_channel=True):
    for key in KEYS_ARM:
        send_channel_message(176, key, 0, 0, midiout[0]) # clear leds
    if paint_channel:
        send_channel_message(176, KEYS_ARM[channel], 127, 0, midiout[0])

def send_channel_message(status, data1=None, data2=None, ch=channel, out=cableout[0]):
    """Send a MIDI channel mode message."""
    msg = [(status & 0xF0) | (ch & 0xF)]

    if data1 is not None:
        msg.append(data1 & 0x7F)
        if data2 is not None:
            msg.append(data2 & 0x7F)

    if data1 is not None and data1 in KEYS_GLOBAL:
        msg[0] = (status & 0xF0) | (GLOBAL_CHAN & 0xF)   # overwrite with global channel

    out.send_message(msg)

def shutdown():
    global midiin, midiout
    print('shutdown ...')
    midiin[0].close_port()
    midiout[0].close_port()
    del midiin
    del midiout

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    shutdown()

import time
import sys
from rtmidi import midiutil

print('connecting maschine')
midiin = midiutil.open_midiinput('Maschine')
midiout = midiutil.open_midioutput('Maschine')
print(midiin)
print(midiout)
# todo route maschine to midi cable (if present)

GROUP = 0
KEYS_GLOBAL = [60, 61, 62, 43, 44, 42, 41, 45]  # transport buttons
KEYS_ARM = [
    48, 49, 50, 51,
    52, 53, 54, 55,  # 0-7 channels mute buttons
    64, 65, 66, 67,  # 8-15 channels arm buttons
    64, 65, 66, 67  # 8-15 channels arm buttons
]


def onmidi(event, data=None):
    message, deltatime = event
    status, note, velocity = message
    print(message)
    iscc = message[0] == 176
    isnote_on = status == 144 and velocity > 0
    isnote_off = status == 144 and velocity == 0
    # isnote_on = velocity == 127
    print(status, note, velocity, 'iscc', iscc, 'isnote_on', isnote_on, 'isnote_off', isnote_off)

    if iscc:
        if isnote_on:
            print(' OKATY , ', note)
            
        elif isnote_off: 
            pass
        else:
            if note == 112:
                print('ALT+F1')
    # pipe messages with the modified channel# virtual midicables
    # send_channel_message(status, note, velocity, channel)


midiin[0].set_callback(onmidi)

# def send_channel_message(status, data1=None, data2=None, ch=GROUP, out=cableout[0]):


def send_channel_message(status, data1=None, data2=None, ch=0, out=midiout[0]):
    """Send a MIDI channel mode message."""
    msg = [(status & 0xF0) | (ch & 0xF)]
    if data1 is not None:
        msg.append(data1 & 0x7F)
        if data2 is not None:
            msg.append(data2 & 0x7F)
    if data1 is not None and data1 in KEYS_GLOBAL:
        # overwrite with global channel
        msg[0] = (status & 0xF0) | (GLOBAL_CHAN & 0xF)
    print(msg)
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

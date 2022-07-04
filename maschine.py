import time
from rtmidi import midiutil

midiin = midiutil.open_midiinput('Maschine')
midiout = midiutil.open_midioutput('Maschine')
print(midiin)
print(midiout)

GROUP = 0
# GROUPS = [ 60, 61, 62, 43, 44, 42, 41, 45 ] # transport buttons
# PADS = [
#     48, 49, 50, 51,
#     52, 53, 54, 55, # 0-7 channels mute buttons
#     64, 65, 66, 67, # 8-15 channels arm buttons
#     64, 65, 66, 67  # 8-15 channels arm buttons
# ]

def onmidi(event, data=None):
    message, deltatime = event
    status, note, velocity = message
    print(message, deltatime)
    print(status, note, velocity)
    iscc = message[0] == 176
    isnote_on = velocity == 127
    print(iscc, isnote_on)
    # pipe messages with the modified channel# virtual midicables
    # send_channel_message(status, note, velocity, channel) 

midiin[0].set_callback(onmidi)

# def paint_leds(paint_channel=True):
#     for key in KEYS_ARM:
#         send_channel_message(176, key, 0, 0, midiout[0]) # clear leds
#     if paint_channel:
#         send_channel_message(176, KEYS_ARM[channel], 127, 0, midiout[0])

# def send_channel_message(status, data1=None, data2=None, ch=GROUP, out=cableout[0]):
def send_channel_message(status, data1=None, data2=None, ch=GROUP):
    """Send a MIDI channel mode message."""
    msg = [(status & 0xF0) | (ch & 0xF)]

    if data1 is not None:
        msg.append(data1 & 0x7F)
        if data2 is not None:
            msg.append(data2 & 0x7F)

    if data1 is not None and data1 in KEYS_GLOBAL:
        # overwrite with global channel
        msg[0] = (status & 0xF0) | (GLOBAL_CHAN & 0xF)

        print_message(msg)
    # out.send_message(msg)


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

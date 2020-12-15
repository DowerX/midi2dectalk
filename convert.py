import mido
from pitches import pitches
import sys

class Event:
    def __init__(self, phoneme, lenght, note):
        self.phoneme = phoneme
        self.lenght = lenght
        self.note = note

    def __str__(self):
        return f"[{self.phoneme}<{self.lenght},{self.note}>]"

def track2dec(inp, phoneme, mspt):
    events = []
    for i in inp:
        if i.type == "note_on":
            events.append(Event("_", round(i.time*mspt), 0))
        elif i.type == "note_off":
            print(noteToFreq(i.note))
            events.append(Event(phoneme, round(i.time*mspt), pitches[noteToFreq(i.note)]))
    return events

def noteToFreq(note):
    a = 440
    return round((a / 32) * (2 ** ((note - 9) / 12)))

def midi2dec(path, phoneme, mpst):
    mid = mido.MidiFile(path)
    for t in mid.tracks:
        events = track2dec(t, phoneme, mpst)
        with open(f"{path}-{t.name}.txt", "w") as f:
            f.write("[:phoneme on]")
            for e in events:
                f.write(str(e))
                #print(str(e))

xbmp = int(sys.argv[2])
xtpb = int(sys.argv[3])
xmspt = (60000/xbmp)/xtpb

midi2dec(sys.argv[1], sys.argv[4], xmspt)
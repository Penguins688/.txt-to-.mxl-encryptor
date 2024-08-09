from music21 import stream, note, duration, chord, pitch, metadata
import os

def map_char_to_note():
    ascii_printable = [chr(i) for i in range(32, 127)]
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'] * 8 
    note_mapping = {}
    
    for i, char in enumerate(ascii_printable):
        octave = i // 12 + 1
        note_name = notes[i] + str(octave)
        note_mapping[char] = note_name
    
    return note_mapping

def create_measure(notes_list, measure_number):
    m = stream.Measure(number=measure_number)
    for note_or_chord, dur, accidental_type in notes_list:
        if note_or_chord == "rest":
            r = note.Rest()
            r.duration = duration.Duration(dur)
            m.append(r)
        elif isinstance(note_or_chord, str):
            n = note.Note(note_or_chord)
            n.duration = duration.Duration(dur)
            if accidental_type:
                n.pitch.accidental = pitch.Accidental(accidental_type.lower())
            m.append(n)
        elif isinstance(note_or_chord, list):
            chord_notes = []
            for pitch_name in note_or_chord:
                n = note.Note(pitch_name)
                chord_notes.append(n)
            c = chord.Chord(chord_notes)
            c.duration = duration.Duration(dur)
            m.append(c)
    return m

def main():
    note_mapping = map_char_to_note()
    
    inFilePath = input("Enter .txt filepath: ")
    content = ""
    with open(inFilePath) as f:
        content = f.read()
    
    score = stream.Score()
    measure_number = 1
    score.metadata = metadata.Metadata()
    score.metadata.composer = "Music21"
    score.metadata.title = os.path.splitext(os.path.basename(inFilePath))[0]
    
    for char in content:
        note_name = note_mapping.get(char, None)
        if note_name:
            notes_list = [(note_name, 4.0, None)]
            measure = create_measure(notes_list, measure_number)
            score.append(measure)
            measure_number += 1
    
    outFilePath = os.path.splitext(inFilePath)[0] + '.mxl'
    score.write('mxl', fp=outFilePath)

if __name__ == "__main__":
    main()

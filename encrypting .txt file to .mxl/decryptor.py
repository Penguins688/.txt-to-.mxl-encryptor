from music21 import converter, note, chord
import os

def map_note_to_char():
    ascii_printable = [chr(i) for i in range(32, 127)]
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'] * 8
    note_mapping = {}
    
    for i, char in enumerate(ascii_printable):
        octave = i // 12 + 1
        note_name = notes[i] + str(octave)
        note_mapping[note_name] = char
    
    return note_mapping

def decrypt_notes_to_text(score):
    note_mapping = map_note_to_char()
    text = ""
    
    for element in score.flatten().notes:
        if isinstance(element, note.Note):
            note_name = element.nameWithOctave
            char = note_mapping.get(note_name, '?')
            text += char
        elif isinstance(element, chord.Chord):
            chord_notes = [n.nameWithOctave for n in element.notes]
            text += "[CHORD]"
    
    return text

def main():
    inFilePath = input("Enter .mxl filepath: ")
    score = converter.parse(inFilePath)
    
    decrypted_text = decrypt_notes_to_text(score)
    
    outFilePath = os.path.splitext(inFilePath)[0] + ".txt"
    with open(outFilePath, 'w') as f:
        f.write(decrypted_text)

if __name__ == "__main__":
    main()
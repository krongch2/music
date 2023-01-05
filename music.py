import re

class Note:

    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self, note_name, octave=4):
        self.note_name = note_name
        self.octave = octave

    def shift(self, halftone=0):
        idx_curr = Note.notes.index(self.note_name)
        semitone_new = idx_curr + halftone
        idx_new = semitone_new % len(Note.notes)
        note_name_new = Note.notes[idx_new]
        octave_new = self.octave + semitone_new // len(Note.notes)
        return Note(note_name_new, octave=octave_new)

    def interval(self, name):
        '''
        https://www.earmaster.com/products/free-tools/interval-song-chart-generator.html
        '''
        interval_halftone_map = {
            0: ['perfect_unison', 'P1'],
            1: ['minor_second', 'm2'],
            2: ['major_second', 'M2'],
            3: ['minor_third', 'm3'],
            4: ['major_third', 'M3'],
            5: ['perfect_fourth', 'P4'],
            6: ['augmented_fourth', 'A4', 'diminished_fifth', 'd5', 'tritone', 'tt'],
            7: ['perfect_fifth', 'P5'],
            8: ['minor_sixth', 'm6', 'augmented_fifth', 'A5'],
            9: ['major_sixth', 'M6', 'diminished_seventh', 'd7'],
            10: ['minor_seventh', 'm7'],
            11: ['major_seventh', 'M7'],
            12: ['perfect_octvae', 'P8']
        }
        for halftone, interval_names in interval_halftone_map.items():
            if name in interval_names:
                break
        return self.shift(halftone=halftone)

    def get_str(self, print_octave=False):
        s = f'{self.note_name}'
        if print_octave:
            s += f'{self.octave}'
        return s

class Notes:

    def __init__(self, notes):
        self.notes = notes

    def get_str(self, print_octave=False):
        l = []
        for note in self.notes:
            l.append(note.get_str(print_octave=print_octave))
        return ' '.join(l)

class Chord(Notes):

    chord_interval_map = {
        # triad
        '': ['P1', 'M3', 'P5'],
        'M': ['P1', 'M3', 'P5'],
        'm': ['P1', 'm3', 'P5'],
        'dim': ['P1', 'm3', 'd5'],
        'aug': ['P1', 'M3', 'A5'],

        # seventh
        'M7': ['P1', 'M3', 'P5', 'M7'],
        'm7': ['P1', 'm3', 'P5', 'm7'],
        '7': ['P1', 'M3', 'P5', 'm7'],
        'dim7': ['P1', 'm3', 'd5', 'd7'],
        'aug7': ['P1', 'M3', 'A5', 'm7']
        }

    def from_symbol(symbol):
        match = re.search('(\w#*)(m|M|dim|aug)*(\d*)', symbol)
        root = match.group(1)
        quality = match.group(2) if match.group(2) is not None else ''
        extension = match.group(3)
        chord_name = quality + extension
        return root, chord_name

    def __init__(self, symbol, octave=4):
        root, chord_name = Chord.from_symbol(symbol)
        self.root = Note(root, octave=octave)
        notes = []
        interval_names = Chord.chord_interval_map[chord_name]
        for interval_name in interval_names:
            notes.append(self.root.interval(interval_name))

        super().__init__(notes)

    def __str__(self):
        return self.get_str()

'''
0 || 1  | 2  | 3  |
E ||-F--|-F#-|-G--|
B ||-C--|-C#-|-D--|
G ||-G#-|-A--|-A#-|
D ||-D#-|-E--|-E#-|
A ||-A#-|-B--|-C--|
E ||-F--|-F#-|-G--|
'''
class Fretboard:
    pass

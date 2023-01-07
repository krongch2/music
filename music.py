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

    def __str__(self):
        return self.get_str()

    def __contains__(self, note):
        '''
        Checks if a note is in this set of notes
        '''
        note_names = [n.note_name for n in self.notes]
        if note.note_name in note_names:
            return True
        else:
            return False

    def from_intervals(root_name, interval_names, octave=4):
        note_root = Note(root_name, octave=octave)
        notes = []
        for interval_name in interval_names:
            notes.append(note_root.interval(interval_name))
        return notes

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
        root_name, chord_name = Chord.from_symbol(symbol)
        self.root = Note(root_name, octave=octave)
        self.chord_name = chord_name
        interval_names = Chord.chord_interval_map[chord_name]
        notes = Notes.from_intervals(root_name, interval_names, octave=octave)
        super().__init__(notes)

class Scale(Notes):

    scale_interval_map = {
        'major': ['P1', 'M2', 'M3', 'P4', 'P5', 'M6', 'M7'],
        'minor': ['P1', 'M2', 'm3', 'P4', 'P5', 'm6', 'm7'],
        'harmonic_minor': ['P1', 'M2', 'm3', 'P4', 'P5', 'm6', 'M7'],
        'major_pentatonic': ['P1', 'M2', 'M3', 'P5', 'P6'],
        'minor_pentatonic': ['P1', 'm3', 'P4', 'P5', 'm7'],
    }

    def __init__(self, root_name, scale_name='major', octave=4):
        self.root = Note(root_name, octave=octave)
        self.scale_name = scale_name
        interval_names = Scale.scale_interval_map[scale_name]
        notes = Notes.from_intervals(root_name, interval_names, octave=octave)
        super().__init__(notes)

class Fretboard:

    def __init__(self, tuning=['E3', 'A3', 'D4', 'G4', 'B4', 'E5'], max_fret=22):
        strings = []
        for open_string in tuning:
            note_name = open_string[0]
            octave = int(open_string[1])
            open_string_note = Note(note_name, octave=octave)
            string = []
            for halftone in range(max_fret + 1):
                string.append(open_string_note.shift(halftone=halftone))
            strings.append(string)
        self.strings = strings

    def display(self, highlight_notes=None, filler='---'):

        def str_format(note_name, filler):
            return f'{filler}{note_name:<2}{filler}'.replace(' ', filler[0])

        def fret0_format(note_name):
            return f'{note_name:<2}||'


        frets_str = [str_format(i, filler=filler) for i in range(1, len(self.strings[0]))]
        fret_label = fret0_format('0') + '|'.join(frets_str)

        strings_str = [fret_label]
        divider = '='*((3 + 2*len(filler))*(len(self.strings[0]) - 1) + 3)
        strings_str.append(divider)
        for string in self.strings[::-1]:
            l = []
            for fret in range(1, len(string)):
                note = string[fret]
                if highlight_notes is None or note in highlight_notes:
                    l.append(str_format(note.note_name, filler=filler))
                else:
                    l.append(str_format('-', filler=filler))
            open_string_note = string[0]
            string_str = fret0_format(open_string_note.note_name) + '|'.join(l)
            strings_str.append(string_str)
        strings_str.append(divider)
        strings_str.append(fret_label)

        display_str = '\n'.join(strings_str)
        print(display_str)

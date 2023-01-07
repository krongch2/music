import music

def test_shift():
    n = music.Note('A', 4)
    print(n.shift(halftone=-5).get_str())
    print(n.shift(halftone=0).get_str())
    print(n.shift(halftone=3).get_str())
    print(n.shift(halftone=12).get_str())
    print(n.shift(halftone=25).get_str())

def test_interval():
    n = music.Note('A', 4)
    print(n.interval('P1').get_str())
    print(n.interval('M3').get_str())
    print(n.interval('P5').get_str())

def test_chord():
    print(music.Chord('C7'))

def test_scale():
    print(music.Scale('A', 'major'))
    print(music.Scale('A', 'minor'))

def test_fretboard():
    f = music.Fretboard()
    f.display()
    f.display(highlight_notes=music.Chord('A'))
    f.display(highlight_notes=music.Scale('A'))

if __name__ == '__main__':
    test_fretboard()

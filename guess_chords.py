# guess_chords.py

def normalize_note(note):
    """
    Normalize a note to a consistent representation (e.g., sharps only).
    :param note: The note to normalize (e.g., "Ab")
    :return: The normalized note (e.g., "G#")
    """
    enharmonic_map = {
        "A#": "Bb", "Bb": "A#",
        "C#": "Db", "Db": "C#",
        "D#": "Eb", "Eb": "D#",
        "F#": "Gb", "Gb": "F#",
        "G#": "Ab", "Ab": "G#"
    }
    return enharmonic_map.get(note, note)

def note_to_semitone(note):
    """
    Convert a note to its semitone value (0-11).
    :param note: Note name (e.g., "C#")
    :return: Semitone value (0-11)
    """
    semitone_map = {
        "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
        "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11
    }
    return semitone_map.get(normalize_note(note))

def semitone_to_note(semitone):
    """
    Convert a semitone value (0-11) to its note name.
    :param semitone: Integer value (0-11)
    :return: Note name (e.g., "C#")
    """
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    return notes[semitone % 12]

def calculate_intervals(notes):
    """
    Guess a chord by calculating intervals relative to each possible root note.
    :param notes: List of notes (e.g., ["F#", "A", "C#"])
    :return: Guessed chord name or "Unknown"
    """
    if not notes:
        return "Unknown"

    # Define chord intervals patterns
    chord_intervals = {
        "Major": [0, 4, 7],
        "minor": [0, 3, 7],
        "Dim": [0, 3, 6],
        "Aug": [0, 4, 8],
        "Maj7": [0, 4, 7, 11],
        "m7": [0, 3, 7, 10],
        "7": [0, 4, 7, 10],  # Dominant 7
        "Dim7": [0, 3, 6, 9],
        "Sus2": [0, 2, 7],
        "Sus4": [0, 5, 7],
        "6": [0, 4, 7, 9],  # Major 6
        "m6": [0, 3, 7, 9],
        "9": [0, 4, 7, 10, 14],  # Dominant 9
        "m9": [0, 3, 7, 10, 14],
        "Maj9": [0, 4, 7, 11, 14]
    }

    # Convert notes to semitones and remove duplicates
    try:
        # Clean up notes and convert to semitones
        cleaned_notes = [note.split('(')[0] for note in notes]  # Remove any text in parentheses
        semitones = sorted(set(note_to_semitone(note) for note in cleaned_notes))
    except (TypeError, KeyError):
        return "Unknown"

    # Debug output
    # print(f"Notes: {cleaned_notes}")
    # print(f"Semitones: {semitones}")

    # Try each note as the potential root
    for root_semitone in semitones:
        # Calculate intervals relative to the root
        intervals = sorted((s - root_semitone) % 12 for s in semitones)

        # Debug output
        # print(f"Root: {semitone_to_note(root_semitone)}, Intervals: {intervals}")

        # Compare with known chord patterns
        for chord_type, pattern in chord_intervals.items():
            if len(intervals) >= 3 and intervals == pattern[:len(intervals)]:
                root_note = semitone_to_note(root_semitone)
                return f"{root_note} {chord_type}"

    # Handle special cases
    if len(semitones) == 2:
        interval = (semitones[1] - semitones[0]) % 12
        root_note = semitone_to_note(semitones[0])

        if interval == 7:  # Perfect fifth
            return f"{root_note} 5"  # Power chord
        elif interval == 4:  # Major third
            return f"{root_note} (no fifth)"
        elif interval == 3:  # Minor third
            return f"{root_note} Minor (no fifth)"

    return "Unknown"

def guess_chord(notes):
    """
    Main function to guess chords using interval calculations.
    :param notes: List of notes (e.g., ["F#", "A", "C#"])
    :return: Guessed chord name or "Unknown"
    """
    if not notes:
        return "Unknown"

    # Handle edge cases
    if len(notes) == 1:
        return f"{notes[0]} (single note)"

    return calculate_intervals(notes)

# Example usage if run directly
if __name__ == "__main__":
    # Test cases
    test_cases = [
        ["F#", "A", "C#"],  # F# minor
        ["C", "E", "G"],    # C major
        ["A", "C", "E"],    # A minor
        ["G", "B", "D"],    # G major
        ["E", "G#", "B"],   # E major
        ["D", "F", "A"],    # D minor
        ["F#", "A#", "C#"], # F# major
    ]

    print("Testing chord detection:")
    for notes in test_cases:
        result = guess_chord(notes)
        print(f"\nNotes: {notes}")
        print(f"Detected chord: {result}")

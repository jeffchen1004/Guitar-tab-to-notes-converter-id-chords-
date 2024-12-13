# tabs_to_notes.py
# Import string_notes from the external file
from string_notes import string_notes
from guess_chords import guess_chord, normalize_note

# Flip the order of the strings for guitar POV: e (high) at the top, E (low) at the bottom
strings_in_order = ['e', 'B', 'G', 'D', 'A', 'E']

# Enharmonic map for notes
enharmonic_map = {
    "A#": "Bb", "Bb": "A#",
    "C#": "Db", "Db": "C#",
    "D#": "Eb", "Eb": "D#",
    "F#": "Gb", "Gb": "F#",
    "G#": "Ab", "Ab": "G#"
}

def format_note_with_enharmonic(note):
    """
    Format a note with its enharmonic equivalent, if applicable.
    :param note: The note to format (e.g., "G#").
    :return: The formatted string (e.g., "G#(Ab)").
    """
    enharmonic = enharmonic_map.get(note, None)
    if enharmonic:
        return f"{note}({enharmonic})" if note.endswith("#") else f"{note}({enharmonic})"
    return note

def format_chord_with_enharmonic(chord):
    """
    Format the guessed chord with its enharmonic equivalent, if applicable.
    :param chord: The guessed chord name (e.g., "F# Minor").
    :return: The formatted chord (e.g., "F#(Gb) Minor").
    """
    if not chord:
        return "Unknown"

    root_note = chord.split()[0]  # Extract the root note (e.g., "F#" from "F# Minor")
    enharmonic = enharmonic_map.get(root_note, None)  # Find enharmonic equivalent
    rest_of_chord = " ".join(chord.split()[1:])  # Get the rest of the chord (e.g., "Minor")

    if enharmonic:
        return f"{root_note}({enharmonic}) {rest_of_chord}"  # Combine with enharmonic
    return chord


# Function to parse input and get corresponding notes
def get_notes(input_tab):
    # Split the input into individual strings and frets
    tabs = input_tab.split(", ")
    result = []
    
    for tab in tabs:
        string, fret = tab[0], int(tab[1:])  # String is the first char, fret is the rest
        raw_note = string_notes[string][fret % 12]  # Get the note (use modulo for octaves)
        formatted_note = format_note_with_enharmonic(raw_note)  # Format the note
        result.append((string, fret, formatted_note))  # Store string, fret, and formatted note as a tuple
    
    return result

# Function to handle cycling input mode
def cycle_input():
    print("Cycle Input Mode: Enter the fret number for each string, or type '-' for no note.")
    result = []
    for string in strings_in_order:
        fret_input = input(f"{string}: ").strip()
        if fret_input == "-":
            continue  # Skip if no note
        try:
            fret = int(fret_input)
            raw_note = string_notes[string][fret % 12]
            formatted_note = format_note_with_enharmonic(raw_note)
            result.append((string, fret, formatted_note))
        except ValueError:
            print(f"Invalid input for {string}. Skipping.")
    return result

# Main program
if __name__ == "__main__":
    print("Choose an input mode:")
    print("1. Manual Input (e.g., A7, D9, G8, B9, e7)")
    print("2. Cycle Input (enter fret for each string individually)")
    mode = input("Enter 1 or 2: ").strip()

    notes = []
    if mode == "1":
        # Manual input mode
        print("Enter strings and fret numbers in the format. ex. A7, D9, G8, B9, e7.")
        print("Separate each entry with a comma and a space.")
        user_input = input("Input: ")
        notes = get_notes(user_input)
    elif mode == "2":
        # Cycle input mode
        notes = cycle_input()
    else:
        print("Invalid choice. Exiting.")
        exit()

    # Display the output
    print("\nNotes:")
    for string in strings_in_order:
        string_notes_display = [f"{string} ({fret}th fret): {note}" for s, fret, note in notes if s == string]
        if string_notes_display:
            print("\n".join(string_notes_display))
        else:
            print(f"{string} (no notes): -")

    # Guess the chord
    note_names = [normalize_note(note.split("(")[0]) for _, _, note in notes]  # Extract normalized note names
    guessed_chord = guess_chord(note_names)

    # Format the guessed chord
    formatted_chord = format_chord_with_enharmonic(guessed_chord)

    print(f"\nGuessed Chord: {formatted_chord}")

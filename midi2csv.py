import mido
import csv
from collections import defaultdict
import math
import sys
import os

def midi_note_to_freq(midi_note):
    return 440 * (2 ** ((midi_note - 69) / 12))

def midi_to_csv(midi_file):
    mid = mido.MidiFile(midi_file)
    
    # Dictionary to store note start times
    note_starts = defaultdict(dict)
    
    # List to store note data
    notes = []

    current_time = 0

    for track in mid.tracks:
        for msg in track:
            current_time += msg.time

            if msg.type == 'note_on' and msg.velocity > 0:
                # Note start
                note_starts[msg.channel][msg.note] = current_time
            elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
                # Note end
                if msg.note in note_starts[msg.channel]:
                    start_time = note_starts[msg.channel][msg.note]
                    duration = current_time - start_time
                    frequency = midi_note_to_freq(msg.note)
                    notes.append([msg.channel, msg.note, duration, frequency])
                    del note_starts[msg.channel][msg.note]

    return notes

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <midi_file>")
        sys.exit(1)

    midi_file = sys.argv[1]
    if not os.path.exists(midi_file):
        print(f"Error: File '{midi_file}' not found.")
        sys.exit(1)

    try:
        notes = midi_to_csv(midi_file)
    except Exception as e:
        print(f"Error processing MIDI file: {e}")
        sys.exit(1)

    # Generate output CSV filename
    base_name = os.path.splitext(os.path.basename(midi_file))[0]
    csv_file = f"{base_name}_output.csv"

    # Write to CSV
    try:
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Channel', 'Pitch', 'Duration', 'Frequency'])
            writer.writerows(notes)
        print(f"CSV file '{csv_file}' has been created.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    

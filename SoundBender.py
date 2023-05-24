import argparse
import os
import wave
import numpy as np


r'''
To use this app, run it from the command line with the required arguments.

Command Line Arguments:
    --input_file: Path to the input audio file.
    --reverse: Reverse the audio.
    --pitch_adjustment: Pitch adjustment value in cents.
    --pitch_divisions: Number of pitch divisions.
    --pitch_direction: Direction of pitch adjustment (up or down).
    --output_prefix: Prefix for output file names.
    --output_folder: Folder to save output files.
    --reverse_order: Generate files in reverse order.

Example Usage:

Linux:
python SoundBender.py --input_file input.wav --pitch_adjustment 300 --pitch_divisions 3 --pitch_direction up 
--output_prefix hum --output_folder output/ --reverse_order --reverse

Windows:
python SoundBender.py --input_file "C:\sounds\input.wav" --pitch_adjustment 300 --pitch_divisions 3 --pitch_direction up 
--output_prefix hum --output_folder "C:\sounds\output" --reverse_order --reverse

This will process the audio file with the specified options and generate output files accordingly.
'''


def reverse_audio(data):
    return data[::-1]


def adjust_pitch(data, pitch_adjustment):
    speed_factor = 2 ** (pitch_adjustment / 1200)
    indices = np.round(np.arange(0, len(data), speed_factor)).astype(int)
    indices = indices[indices < len(data)].tolist()  # Convert indices to a list
    adjusted_data = data[indices]
    return adjusted_data


def process_audio_file(input_file, reverse, pitch_adjustment, pitch_divisions, pitch_direction, output_prefix,
                       output_folder, reverse_order):
    print("Processing audio file...")
    print(f"Input file: {input_file}")
    print(f"Reverse: {reverse}")
    print(f"Pitch adjustment: {pitch_adjustment} cents")
    print(f"Pitch divisions: {pitch_divisions}")
    print(f"Pitch direction: {pitch_direction}")
    print(f"Output prefix: {output_prefix}")
    print(f"Output folder: {output_folder}")
    print(f"Reverse order: {reverse_order}")
    print()

    # Load the input file
    try:
        with wave.open(input_file, 'rb') as wav_file:
            num_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            frame_rate = wav_file.getframerate()
            num_frames = wav_file.getnframes()
            audio_data = np.frombuffer(wav_file.readframes(num_frames), dtype=np.int16)

        if reverse:
            audio_data = reverse_audio(audio_data)

        if pitch_adjustment != 0:
            pitch_step = pitch_adjustment / (pitch_divisions - 1)

            if pitch_direction == 'down':
                pitch_adjustments = np.arange(0, -pitch_adjustment - pitch_step, -pitch_step)
            else:
                pitch_adjustments = np.arange(0, pitch_adjustment + pitch_step, pitch_step)

            if reverse_order:
                pitch_adjustments = pitch_adjustments[::-1]

            for i, adjustment in enumerate(pitch_adjustments, start=1):
                adjusted_data = adjust_pitch(audio_data, adjustment)
                save_output_file(adjusted_data.tobytes(), num_channels, sample_width, frame_rate, output_prefix,
                                 output_folder, i)

        else:
            save_output_file(audio_data.tobytes(), num_channels, sample_width, frame_rate, output_prefix, output_folder)

        print("Audio processing completed successfully.")
    except Exception as e:
        print("An error occurred during audio processing.")
        print(f"Error message: {str(e)}")


def save_output_file(data, num_channels, sample_width, frame_rate, output_prefix, output_folder, index=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_filename = f"{output_prefix}"
    if index is not None:
        output_filename += f"({index})"
    output_filename += ".wav"

    existing_files = [f for f in os.listdir(output_folder) if f.startswith(output_prefix)]
    if existing_files:
        existing_indices = [get_index_from_filename(f) for f in existing_files]
        next_index = max(existing_indices) + 1
        output_filename = f"{output_prefix}({next_index}).wav"

    output_path = os.path.join(output_folder, output_filename)

    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(frame_rate)
        wav_file.writeframes(data)

    print(f"Saved output file: {output_path}")


def get_index_from_filename(filename):
    start_index = filename.find('(')
    end_index = filename.find(')')
    if start_index != -1 and end_index != -1:
        try:
            index = int(filename[start_index + 1: end_index])
            return index
        except ValueError:
            pass
    return None


def main():
    parser = argparse.ArgumentParser(description='Sound Bender - Audio Processing App')
    parser.add_argument('--input_file', type=str, help='Path to the input audio file')
    parser.add_argument('--reverse', action='store_true', help='Reverse the audio')
    parser.add_argument('--pitch_adjustment', type=int, default=0, help='Pitch adjustment value in cents')
    parser.add_argument('--pitch_divisions', type=int, default=1, help='Number of pitch divisions')
    parser.add_argument('--pitch_direction', choices=['up', 'down'], default='up', help='Direction of pitch adjustment')
    parser.add_argument('--output_prefix', type=str, default='output', help='Prefix for output file names')
    parser.add_argument('--output_folder', type=str, default='output', help='Folder to save output files')
    parser.add_argument('--reverse_order', action='store_true', help='Generate files in reverse order')
    args = parser.parse_args()

    process_audio_file(args.input_file, args.reverse, args.pitch_adjustment, args.pitch_divisions,
                       args.pitch_direction, args.output_prefix, args.output_folder, args.reverse_order)


if __name__ == '__main__':
    main()

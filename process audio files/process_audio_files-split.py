import os
import random
from pydub import AudioSegment

def is_audio_playable(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        return True
    except Exception as e:
        return False

def is_audio_file(file_extension):
    audio_extensions = ['.aif', '.aiff', '.wav', '.opus', '.mp3', '.aac', '.flac', '.ogg']
    return file_extension.lower() in audio_extensions

def process_audio_files(directory):
    for root, dirs, files in os.walk(directory):
        counter = 0
        for file in files:
            if file.startswith('.'):
                continue

            old_file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1]

            if not is_audio_file(file_extension):
                print(f"Skipping non-audio file: {old_file_path}")
                continue

            if not is_audio_playable(old_file_path):
                print(f"Deleting unplayable file: {old_file_path}")
                os.remove(old_file_path)
                continue

            new_file_name = '{:02d}{}'.format(counter, file_extension)
            new_file_path = os.path.join(root, new_file_name)

            while os.path.exists(new_file_path):
                counter += 1
                new_file_name = '{:02d}{}'.format(counter, file_extension)
                new_file_path = os.path.join(root, new_file_name)

            os.rename(old_file_path, new_file_path)

            audio = AudioSegment.from_file(new_file_path)
            if len(audio) > 20 * 60 * 1000:
                segment_dir = os.path.join(root, 'segments')
                segment_length_ms = random.randint(10 * 60 * 1000, 20 * 60 * 1000)

                for i in range(0, len(audio), segment_length_ms):
                    end = min(i + segment_length_ms, len(audio))
                    segment = audio[i:end]

                    if not os.path.exists(segment_dir):
                        os.makedirs(segment_dir, exist_ok=True)

                    segment_filename = f'{counter}_segment_{i//segment_length_ms}{file_extension}'
                    segment.export(os.path.join(segment_dir, segment_filename), format=file_extension[1:])

                os.remove(new_file_path)
            counter += 1

    print('Audio file processing done!')

# Example usage
root_directory = r"D:\reference_dataset"
process_audio_files(root_directory)

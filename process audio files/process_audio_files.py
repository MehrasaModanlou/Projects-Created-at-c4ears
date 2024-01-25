import os
from pydub import AudioSegment

def is_audio_playable(file_path):
   try:
       audio = AudioSegment.from_file(file_path)
       return True
   except Exception as e:
       return False

def is_audio_file(file_extension):
   # List of supported audio file extensions
   audio_extensions = ['.aif', '.aiff', '.wav', '.opus', '.mp3', '.aac', '.flac', '.ogg']
   return file_extension.lower() in audio_extensions

def rename_files(directory):
   for root, dirs, files in os.walk(directory):
       counter = 0 # Reset counter for each new directory
       for file in files:
           old_file_path = os.path.join(root, file)
           file_extension = os.path.splitext(file)[1] # Get the extension with the dot

           # Skip directories, special files, and hidden files
           if file.startswith('.') or not is_audio_file(file_extension):
               print(f"Removing hidden or non-audio file: {old_file_path}")
               os.remove(old_file_path)
               continue

           new_file_name = '{:02d}{}'.format(counter, file_extension)
           new_file_path = os.path.join(root, new_file_name)

           # Check if the file is playable
           if not is_audio_playable(old_file_path):
               print(f"Removing unplayable file: {old_file_path}")
               os.remove(old_file_path)
               continue

           # Ensure the new file name doesn't already exist
           while os.path.exists(new_file_path):
               counter += 1
               new_file_name = '{:02d}{}'.format(counter, file_extension)
               new_file_path = os.path.join(root, new_file_name)

           os.rename(old_file_path, new_file_path)
           counter += 1

   print('Rename done!')

# Provide the root directory where you want to start renaming files
root_directory = r"Z:\temp\reference"

rename_files(root_directory)

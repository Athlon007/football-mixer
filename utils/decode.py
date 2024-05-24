# Description:  This script is used to decode the audio files based on the tags
# provided in the CSV file and save the clips to the output folder.
#
# Author: Konrad Figura

from concurrent.futures import ThreadPoolExecutor, as_completed
from pydub import AudioSegment
import os
import pandas as pd

# CHANGE DATA AS YOU NEED
file_path = '/Users/konradfigura/dataset/first_45_mins_tags.csv' # Path to the CSV file containing the tags
audio_folder_path = '/Users/konradfigura/dataset/Main2' # Folder containing the audio files
output_folder_path = '/Users/konradfigura/dataset/Clips' # Folder to save the clips
max_workers = 4 # Number of threads to use for processing audio files (how many files to process at the same time)

# Load the CSV file to check its structure
tags_df = pd.read_csv(file_path)
created_directories = set()  # Keep track of already created directories

# Convert timecode (HH:MM:SS:FF) to milliseconds, assuming 24 fps
def timecode_to_milliseconds(timecode):
    hours, minutes, seconds, frames = [int(x) for x in timecode.split(':')]
    return ((hours * 3600 + minutes * 60 + seconds) * 1000) + int((frames / 24) * 1000)

# Function to process a single audio file
def process_audio_file(row, audio, output_folder):
    start_time = timecode_to_milliseconds(row['Timecode In'])
    end_time = timecode_to_milliseconds(row['Timecode Out'])
    clip = audio[start_time:end_time]

    label_folder = os.path.join(output_folder, row['Description'].lower())

    # Check if we've already created this directory in this session
    if label_folder not in created_directories:
        os.makedirs(label_folder, exist_ok=True)  # exist_ok=True avoids error if directory already exists
        created_directories.add(label_folder)

    output_path = os.path.join(label_folder, f"clip_{row.name}.wav")
    clip.export(output_path, format="wav")
    return f"Exported: {output_path}"

# Main function to process audio files using multiple threads
def process_audio_files(df, audio_folder, output_folder):
   # Create object that caches audio file (one file at a time)
   audio_file = None
   audio_file_name = None
   # Go through each row in the dataframe and process the audio file
   for index, row in df.iterrows():
        # Get trackname column.
        track_name = row['Track name'] + ".wav"

        # Does file exist?
        if not os.path.exists(os.path.join(audio_folder, track_name)):
            print(f"File not found: {track_name}")
            continue

        # Is the audio file already cached?
        if audio_file is None or audio_file_name != track_name:
            # If not, load it and cache it.
            audio_file_name = track_name
            print(f"Loading {track_name}")
            audio_file = AudioSegment.from_wav(os.path.join(audio_folder, track_name))
            print(f"Loaded {track_name}")
        else:
            print(f"Already loaded {track_name}")

        # Process
        print(f"Processing {row['Description']} from {track_name}")
        result = process_audio_file(row, audio_file, output_folder)
        print(result)
        print("\n")


# Split df into chunks corresponding to the number of workers
chunk_size = len(tags_df) // max_workers
chunks = [tags_df.iloc[i:i + chunk_size] for i in range(0, len(tags_df), chunk_size)]
print(f"Split the dataframe into {len(chunks)} chunks")
print(f"Chunk size: {chunk_size}")

# Process each chunk in a separate thread
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(process_audio_files, chunk, audio_folder_path, output_folder_path) for chunk in chunks]
    for future in as_completed(futures):
        print(future.result())
        print("\n")
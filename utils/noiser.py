# noiser
# Loads all audio files in directory, takes random timestamps and cuts 1 second
# of audio from that timestamp and saves into destination directory.
#
# Author: Konrad Figura

import os
import random
import wave
import contextlib
import soundfile as sf

# get read and write directories from command line
import sys
if len(sys.argv) != 3:
    print("Usage: python3 noiser.py <read_directory> <write_directory>")
    sys.exit()

read_directory = sys.argv[1]
write_directory = sys.argv[2]

# get all files in directory
files = os.listdir(read_directory)

# create 'clips' directory if it doesn't exist
if not os.path.exists(write_directory):
    os.makedirs(write_directory)

# iterate through all files
for file in files:
    # check if file is a .wav file
    if file.endswith(".wav"):
        # load file
        with contextlib.closing(wave.open(read_directory + "/" + file,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            # load file
            data, rate = sf.read(read_directory + "/" + file)

            # calculate how many clips to create. For each 15 seconds of audio, create 1 clip
            num_clips = int(duration / 15)

            # create 3 random clips
            for i in range(num_clips):
                # create random timestamp
                timestamp = random.uniform(0, duration-1)
                # create new file name
                new_file = file.split(".")[0] + "_" + str(i) + ".wav"
                # create new file
                new_data = data[int(timestamp*rate):int((timestamp+1)*rate)]
                sf.write(write_directory + "/" + new_file, new_data, rate)
                print("Created " + new_file)


print("Done!")
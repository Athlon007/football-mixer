# AudioRanClip
# Loads all audio files in directory and creates 3 copies of each file
# with first starting at 0s to 1/2 of the duration, second starting at 1/2 of
# the duration to the end and third starting at 1/4th of the duration
# and ending at 3/4th of the duration.
#
# Author: Konrad Figura

import os
import random
import wave
import contextlib
import soundfile as sf

# get dir from command line
import sys
if len(sys.argv) != 2:
    print("Usage: python3 AudioRanClip.py <directory>")
    sys.exit()

directory = sys.argv[1]

# get all files in directory
files = os.listdir(directory)

# create 'clips' directory if it doesn't exist
if not os.path.exists(directory + "/clips"):
    os.makedirs(directory + "/clips")

# iterate through all files
for file in files:
    # check if file is a .wav file
    if file.endswith(".wav"):
        # load file
        with contextlib.closing(wave.open(directory + "/" + file,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            # load file
            data, rate = sf.read(directory + "/" + file)
            # create 3 random clips
            for i in range(2):
                # create new file name
                new_file = file.split(".")[0] + "_" + str(i) + ".wav"
                # create new file
                # Remember that first must be half of the duration, then 2nd is second half
                if i == 0:
                    new_data = data[:int(duration/2*rate)]
                else:
                    new_data = data[int(duration/2*rate):]

                sf.write(directory + "/clips/" + new_file, new_data, rate)
                print("Created " + new_file)

            # create 3rd one that starts at 1/4th of the duration and ends at 3/4th of the duration
            new_file = file.split(".")[0] + "_2.wav"
            new_data = data[int(duration/4*rate):int(3*duration/4*rate)]
            sf.write(directory + "/clips/" + new_file, new_data, rate)
            print("Created " + new_file)


print("Done!")
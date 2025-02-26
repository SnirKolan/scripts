import subprocess
import os
import argparse

#User parameters
parser = argparse.ArgumentParser(description="Extract from Video")
parser.add_argument('--video', type=str, required=True,
                    help="Name of the video to extract.")
parser.add_argument('--fps', type=int, default=1,
                    help="How many jpegs we want per second of video")
parser.add_argument('--starttime', type=int, default=None,
                    help="Time in seconds that we want to start extracting from")
parser.add_argument('--endtime', type=int, default=None,
                    help="Time in seconds that we want to finish extracting at")               
args = parser.parse_args()

input_video = args.video #filename.mkv
desired_jpegs_per_sec = args.fps
start_time = args.starttime
end_time = args.endtime

#Create dir, and add number if it already exists
base_output_dir = os.path.splitext(os.path.basename(input_video))[0]
output_dir = base_output_dir
counter = 1

while os.path.exists(output_dir):
    output_dir = f"{base_output_dir}_{counter}"
    counter += 1

os.makedirs(output_dir, exist_ok=True)
output_pattern = os.path.join(output_dir, 'frame_%04d.jpg')

# FFmpeg command to extract the desired number of frames per second
command = ['ffmpeg']

#Add start and end time in seconds if specified
if start_time is not None:
    command += ['-ss', str(start_time)]
if end_time is not None:
    command += ['-to', str(end_time)]

command += ['-i', input_video, '-vf', f'fps={desired_jpegs_per_sec}', output_pattern]

subprocess.run(command)
print("Done extracting frames!")
import subprocess
import os
import argparse
import tempfile


def create_images_dir(original_file_name):
    base_output_dir = original_file_name
    output_dir = base_output_dir
    dir_counter = 1

    while os.path.exists(output_dir):
        output_dir = f"{base_output_dir}_{dir_counter}"
        dir_counter += 1

    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def remux_video(input_video):
    print("Remuxing video for reliable extraction...")

    file_extension = os.path.splitext(os.path.basename(input_video))[1]
    if not file_extension:
        file_extension = '.mkv'  # Default if no extension is found

    with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as tmp_file:
        remuxed_video = tmp_file.name
    
    remux_command = ['ffmpeg', '-y', '-i', input_video, '-c', 'copy', remuxed_video]
    subprocess.run(remux_command, check=True)
    print("Remuxing complete.")
    return remuxed_video

def extract_frames(file_name, output_dir, desired_jpegs_per_sec, start_time = None, end_time = None, quality = 2):
    output_pattern = os.path.join(output_dir, 'frame_%04d.jpg')
    print("Extracting frames...")
    # FFmpeg command to extract the desired frames
    command = ['ffmpeg']

    #Add start and end time in seconds if specified
    if start_time is not None:
        command += ['-ss', str(start_time)]
    if end_time is not None:
        command += ['-to', str(end_time)]

    command += ['-i', file_name, '-vf', f'fps={desired_jpegs_per_sec}', '-q:v', str(quality), output_pattern]

    subprocess.run(command)
    print("Done extracting frames!")

def run():
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
    parser.add_argument('--remux', action='store_true',
                        help="Remux the video before extracting (may help with corrupted files)")
            

    args = parser.parse_args()

    video_file_name = args.video #filename.mkv
    should_remax_video = args.remux

    #Create dir for the images
    video_name = os.path.splitext(os.path.basename(video_file_name))[0]
    output_dir = create_images_dir(video_name)

    #Remux video to ensure reliable extraction
    if should_remax_video:
        video_file_name = remux_video(video_file_name)
        extract_frames(video_file_name, output_dir, args.fps, args.starttime, args.endtime)
        os.remove(video_file_name)
    else:
        extract_frames(video_file_name, output_dir, args.fps, args.starttime, args.endtime)
run()
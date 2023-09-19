import subprocess

# for video
def resize_video(input_path, output_path, resolution):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f'scale={resolution}',
        '-c:a', 'copy',
        output_path
    ]
    subprocess.run(command)

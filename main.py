import os
import sys
import glob
import subprocess


ROOT_PATH = sys.argv[1]
LIMIT_FILE_SIZE = 1.8 * 1024 * 1024 * 1024
TARGET_FILE_SIZE = 1.5 * 1024 * 1024 * 1024
DEFAULT_BIT_RATE = 2_000


files = glob.glob(f'{ROOT_PATH}/*.mp4')

for file_path in files:
    output_name = f'{file_path[:-4]}.min.mp4'
    file_size = os.path.getsize(file_path)

    if file_size < LIMIT_FILE_SIZE or output_name in files:
        continue

    file_size = os.path.getsize(file_path)
    print(f'output-name: {output_name}, file-size: {file_size}, file-name: {file_path}')
    subprocess.run(f'ffmpeg -i "{file_path}" -b:v {DEFAULT_BIT_RATE}k "{output_name}"', shell=True)
    output_file_size = os.path.getsize(output_name)
    if output_file_size > LIMIT_FILE_SIZE:
        os.remove(output_name)
        bit_rate = int(TARGET_FILE_SIZE / output_file_size * DEFAULT_BIT_RATE)
        print(f'file:{file_path}, bit-rate:{bit_rate}')
        subprocess.run(f'ffmpeg -i "{file_path}" -b:v {bit_rate}k "{output_name}"', shell=True)

    os.remove(file_path)
    subprocess.run(f'mv "{output_name}" "{file_path}"', shell=True)

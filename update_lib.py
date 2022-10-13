import os
import shutil
import subprocess


working_dir = os.path.dirname(os.path.abspath(__file__))
lib_name = 'jto'


print('Remove previous build directories')
for filename in os.listdir(working_dir):
    if filename in ['build', 'dist'] or '.egg-info' in filename:
        print(f'Remove directory {filename}')
        shutil.rmtree(filename)

print(f'Unistall current version of library from interpreter')
subprocess.Popen(["pip", "uninstall", lib_name, "-y"]).wait()

print(f'Install library to current interpreter')
subprocess.Popen(["pip", "install", working_dir]).wait()

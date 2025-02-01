from os import path, listdir, mkdir
from shutil import copy, rmtree

def copy_contents(from_dir, to_dir):
    if path.exists(to_dir):
        rmtree(to_dir)
    mkdir(to_dir)
    for entry in listdir(from_dir):
        current_fullpath = path.join(from_dir, entry)
        dest_fullpath = path.join(to_dir, entry)
        if path.isfile(current_fullpath):
            print(f"Copying {current_fullpath} to {dest_fullpath}")
            copy(current_fullpath, dest_fullpath)
        else:
            mkdir(dest_fullpath)
            copy_contents(current_fullpath, dest_fullpath)
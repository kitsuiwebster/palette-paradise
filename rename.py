import os
import base64
import random
import string

def generate_random_base64_string(length):
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    base64_string = base64.urlsafe_b64encode(random_string.encode()).decode().strip('=')
    return base64_string[:16]

def rename_png_files(directory):
    print(f"Renaming files in directory: {directory}")
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            new_filename = generate_random_base64_string(16) + ".png"
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f"Renamed {filename} to {new_filename}")
        else:
            print(f"Skipping {filename} as it is not a .png file")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    directory = os.path.join(current_dir, 'to_be_renamed')
    rename_png_files(directory)
    print("All .png files have been renamed.")

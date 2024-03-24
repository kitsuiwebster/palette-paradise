import os
import shutil
from PIL import Image

def resize_image(image_path, output_size):
    print(f"👉 Resizing image: {os.path.basename(image_path)} to {output_size[0]}x{output_size[1]}")
    with Image.open(image_path) as img:
        resized_img = img.resize(output_size, Image.LANCZOS)
    return resized_img

def process_images_in_directory(raw_directory="./raw", packed_directory="./packed"):
    target_width = 1792
    target_height = 2688
    sizes = [(896, 1344), (1344, 2016), (2240, 3360), (2688, 4032)] 
    print("👉 Starting image processing...")

    for filename in os.listdir(raw_directory):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif')):
            image_path = os.path.join(raw_directory, filename)
            with Image.open(image_path) as img:
                if img.width == target_width and img.height == target_height:
                    print(f"👉 Found matching image: {filename}")
                    base_name = os.path.splitext(filename)[0]
                    new_dir_path = os.path.join(packed_directory, base_name)
                    os.makedirs(new_dir_path, exist_ok=True)
                    print(f"👉 Created directory: {new_dir_path}")

                    # Generate and save resized images.
                    for size in sizes:
                        resized_img = resize_image(image_path, size)
                        new_filename = f"{base_name}_{size[0]}x{size[1]}.png"
                        resized_img.save(os.path.join(new_dir_path, new_filename))
                        print(f"👉 Saved resized image: {new_filename}")

                    # Move and rename the original image.
                    new_original_path = os.path.join(new_dir_path, f"{base_name}_{target_width}x{target_height}.png")
                    shutil.copy2(image_path, new_original_path)
                    print(f"👉 Copied and renamed original image to: {new_original_path}")
                else:
                    print(f"👉 Skipping non-matching image: {filename}")
    print("✅ Image processing completed.")

if __name__ == "__main__":
    process_images_in_directory()

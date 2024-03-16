from PIL import Image
import os

def create_output_folder(image_path):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    folder_name = f'./ready/{base_name}_output'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def save_image(image, folder_name, filename):
    path = os.path.join(folder_name, filename)
    image.save(path)
    print(f'File generated: {path}')

def crop_to_aspect_ratio(image, target_width, target_height):
    original_width, original_height = image.size

    target_ratio = target_width / target_height
    original_ratio = original_width / original_height

    if original_ratio > target_ratio:
        new_width = int(target_ratio * original_height)
        new_height = original_height
        left = (original_width - new_width) / 2
        top = 0
    else:
        new_height = int(original_width / target_ratio)
        new_width = original_width
        left = 0
        top = (original_height - new_height) / 2

    right = left + new_width
    bottom = top + new_height

    return image.crop((left, top, right, bottom))

def upscale_and_resize_2x3(image_path, output_sizes):
    folder_name = create_output_folder(image_path)
    img = Image.open(image_path)

    upscaled_img = img.resize(output_sizes[0], Image.Resampling.BICUBIC)
    upscaled_filename = f'upscaled_{output_sizes[0][0]}x{output_sizes[0][1]}_2x3.png'
    save_image(upscaled_img, folder_name, upscaled_filename)

    for size in output_sizes[1:]:
        resized_img = upscaled_img.resize(size, Image.Resampling.BICUBIC)
        resized_filename = f'resized_{size[0]}x{size[1]}_2x3.png'
        save_image(resized_img, folder_name, resized_filename)

def upscale_and_resize_3x4(image_path, output_sizes):
    folder_name = create_output_folder(image_path)
    img = Image.open(image_path)

    for size in output_sizes:
        cropped_img = crop_to_aspect_ratio(img, *size)
        resized_img = cropped_img.resize(size, Image.Resampling.BICUBIC)
        filename = f'cropped_{size[0]}x{size[1]}_3x4.png'
        save_image(resized_img, folder_name, filename)

def crop_to_square_and_resize(image_path, output_size):
    folder_name = create_output_folder(image_path)
    img = Image.open(image_path)
    cropped_img = crop_to_aspect_ratio(img, output_size[0], output_size[1])
    square_img = cropped_img.resize(output_size, Image.Resampling.BICUBIC)
    square_filename = f'squared_{output_size[0]}x{output_size[1]}_1x1.png'
    save_image(square_img, folder_name, square_filename)

def process_images(image_paths, output_sizes_2x3, output_sizes_3x4, output_size_square):
    for image_path in image_paths:
        print(f'Processing {image_path}')
        upscale_and_resize_2x3(image_path, output_sizes_2x3)
        upscale_and_resize_3x4(image_path, output_sizes_3x4)
        crop_to_square_and_resize(image_path, output_size_square)
        print(f"All files for {image_path} have been successfully generated.")

def get_all_files_in_folder(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# List of image paths
image_paths = get_all_files_in_folder('raw')

# Output sizes
output_sizes_2x3 = [(1440, 2160), (1080, 1620), (2560, 3840)]
output_sizes_3x4 = [(2048, 2732), (1200, 1600), (960, 1280)]
output_size_square = (2000, 2000)

# Process all images
process_images(image_paths, output_sizes_2x3, output_sizes_3x4, output_size_square)

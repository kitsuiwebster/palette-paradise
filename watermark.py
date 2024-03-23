import os
from PIL import Image

# Define the directories
input_dir = './raw'
watermark_path = './assets/watermark.png'
output_dir = './watermarked'

# Check if output directory exists, if not, create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the watermark image once
watermark = Image.open(watermark_path)

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    # Check if the file is an image
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        print(f'👉 Processing {filename}...')

        # Open the image
        img = Image.open(os.path.join(input_dir, filename))

        # Check if the image size is larger than the watermark
        if img.width >= watermark.width and img.height >= watermark.height:
            # Create a layer image with the same size as the input image
            layer = Image.new('RGBA', img.size, (0,0,0,0))

            # Paste the watermark onto the layer
            layer.paste(watermark, (img.width - watermark.width, img.height - watermark.height), mask=watermark)

            # Paste the layer onto the input image
            img = Image.composite(layer, img, layer)

            # Save the watermarked image
            img.save(os.path.join(output_dir, filename))
            print(f'👉 Watermarked image saved as {output_dir}/{filename}')
        else:
            print(f'👉 Skipping {filename}. Image size is smaller than the watermark.')
    else:
        print(f'👉 Skipping {filename}. File is not an image.')

print('✅ All images have been processed.')

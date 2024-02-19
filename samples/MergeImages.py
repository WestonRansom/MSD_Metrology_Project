from PIL import Image
import os

# Hardcoded directory containing the images
directory = r"C:\Users\westontest\OneDrive - rit.edu\Fifth Year\MSD\WestonCameraTest\tisgrabber\samples\images\\"

# Check if the directory exists
if os.path.isdir(directory):
    image_filenames = [f"image{i}.jpg" for i in range(1, 49)]

    # Load and resize images without padding
    thumbnail_images = []
    for filename in image_filenames:
        img = Image.open(os.path.join(directory, filename))
        img_resized = img.resize((200, 200), Image.BICUBIC)  # Adjust size as needed
        thumbnail_images.append(img_resized)

    # Arrange images according to the specified pattern for a 5x9 grid
    image_order = [
        41, 42, 43, 44, 45,
        36, 37, 38, 39, 40,
        31, 32, 33, 34, 35,
        26, 27, 28, 29, 30,
        21, 22, 23, 24, 25,
        16, 17, 18, 19, 20,
        11, 12, 13, 14, 15,
        6, 7, 8, 9, 10,
        1, 2, 3, 4, 5
    ]

    # Select the images in the specified order (handle cases where fewer than 48 images are available)
    arranged_images = [thumbnail_images[i - 1] for i in image_order if i <= len(thumbnail_images)]

    # Calculate dimensions for the merged image
    columns = 5
    rows = (len(arranged_images) + columns - 1) // columns  # Calculate total rows needed
    merged_width = columns * thumbnail_images[0].width
    merged_height = rows * thumbnail_images[0].height

    # Create a blank canvas for the merged image
    merged_image = Image.new('RGB', (merged_width, merged_height), (250, 250, 250))

    # Paste thumbnails into the merged image following the specified pattern
    for i, img in enumerate(arranged_images):
        col = i % columns
        row = i // columns
        x_offset = col * img.width
        y_offset = row * img.height
        merged_image.paste(img, (x_offset, y_offset))

    # Resize the final merged image to a larger high-quality version
    final_size = (merged_width * 4, merged_height * 4)  # Increase size to 4 times the original
    final_image = merged_image.resize(final_size, Image.BICUBIC)  # BICUBIC for high-quality resize

    # Save the final merged image in the same directory as the input images
    output_path = os.path.join(directory, "final_merged_image.jpg")
    final_image.save(output_path, "JPEG")
    final_image.show()
else:
    print("Invalid directory. Please provide a valid directory path containing images.")

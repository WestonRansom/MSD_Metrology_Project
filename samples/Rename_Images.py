from PIL import Image
import os

# Set the path to your directory containing the images
directory = r"C:\Users\westontest\OneDrive - rit.edu\Fifth Year\MSD\WestonCameraTest\tisgrabber\samples\images\\"

# List all files in the directory
files = os.listdir(directory)

# Filter only the image files
image_files = [file for file in files if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png')]

# Sort the image files based on their creation time (oldest to newest)
image_files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)))

# Rotate and rename the files sequentially
for index, file in enumerate(image_files, start=1):
    # Open the image
    img = Image.open(os.path.join(directory, file))

    # Rotate the image clockwise (90 degrees)
    rotated_img = img.rotate(90, expand=True)

    # Save the rotated image with the new name
    new_name = f'image{index}.jpg'  # Create the new name
    rotated_img.save(os.path.join(directory, new_name))  # Save the rotated image
    print(f'Rotated and renamed {file} to {new_name}')

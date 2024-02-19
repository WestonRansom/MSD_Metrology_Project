from PIL import Image, ImageFilter, ImageChops
import os
import cv2
import numpy as np


# Hardcoded directory containing the images
directory = r"C:\Users\westontest\OneDrive - rit.edu\Fifth Year\MSD\WestonCameraTest\tisgrabber\samples\images"

# Check if the directory exists
if os.path.isdir(directory):
    # Generate image filenames for 36 images
    image_filenames = [f"image{i}.jpg" for i in range(1, 37)]

    # Load original images
    original_images = [Image.open(os.path.join(directory, filename)) for filename in image_filenames]

    # Calculate dimensions for the merged image
    columns = 6
    rows = 6  # 36 images will fit in a 6x6 grid
    merged_width = columns * original_images[0].width
    merged_height = rows * original_images[0].height

    # Create a blank canvas for the merged image
    merged_image = Image.new('RGB', (merged_width, merged_height), (250, 250, 250))

    # Paste original images into the merged image in a grid
    for i, img in enumerate(original_images):
        col = i % columns
        row = i // columns
        x_offset = col * img.width
        y_offset = row * img.height
        merged_image.paste(img, (x_offset, y_offset))

    # Save the final merged image in the same directory as the input images
    output_path = os.path.join(directory, "final_merged_image.jpg")
    merged_image.save(output_path, "JPEG")
    print("Images Merged Successfully!")

    '''Image.MAX_IMAGE_PIXELS = None
    # Open the resized image to avoid decompression bomb error
    resized_image = Image.open(output_path)

    # Converting the image to grayscale, as Sobel Operator requires
    # input image to be of mode Grayscale (L)
    img_gray = resized_image.convert("L")

    # Calculating Edges using the passed Laplacian Kernel
    #edges_image = img_gray.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8, -1, -1, -1, -1), 1, 0))
    edges_image = img_gray.filter(ImageFilter.FIND_EDGES)
    # Invert the edges image
    inverted_edges_image = ImageChops.invert(edges_image)
    inverted_edges_image.save(os.path.join(directory, "Inverted_EDGE_sample.png"), "PNG")'''
    # Save the inverted edges image

    # Read the image
    img = cv2.imread(r"C:\Users\westontest\OneDrive - rit.edu\Fifth Year\MSD\WestonCameraTest\tisgrabber\samples\images\final_merged_image.jpg", cv2.IMREAD_GRAYSCALE)
    # Apply thresholding
    _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Draw contours on a copy of the original image
    contour_image = np.copy(img)
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
    output_path = os.path.join(directory, "Inverted_EDGE_sample.png")
    cv2.imwrite(output_path, contour_image)



    print("Image Filtered Successfully!")


else:
    print("Invalid directory. Please provide a valid directory path containing images.")



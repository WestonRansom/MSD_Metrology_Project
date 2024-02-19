from pyimagej import ImageJ
import os

# Set the path to the ImageJ installation directory
ij_dir = r"C:\Users\westontest\Downloads\fiji-win64\Fiji.app"  # Replace with your actual ImageJ installation path

# Start PyImageJ
ij = ImageJ(ij_dir)

# Load images from the folder
folder_path = r"C:\Users\westontest\OneDrive - rit.edu\Fifth Year\MSD\WestonCameraTest\tisgrabber\samples\images"
images = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(".jpg")]

# Load the images into an ImageJ virtual stack
virtual_stack = ij.py.show(images, title="Image Stack")

# Run the Grid/Collection stitching plugin
# Adjust the parameters based on your images and stitching requirements
ij.py.run_macro("""run("Grid/Collection stitching", "type=[Grid: snake by rows] order=[Right & Down ] grid_size_x=6 grid_size_y=6 tile_overlap=10 first_file_index_i=1 directory='/path/to/output/folder' file_names='Image_%s.jpg' output_textfile_name='/path/to/output/folder/stitching_grid.txt' fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 compute_overlap subpixel_accuracy compute_overlap");""")
# Make sure to replace '/path/to/output/folder' with your actual output folder path

# Save the stitched image
output_path = r"C:\Users\westontest\OneDrive - rit.edu\Fifth Year\MSD\WestonCameraTest\tisgrabber\samples\images\stitched_image.jpg"
ij.py.save_as_jpeg(virtual_stack, output_path)

# Stop PyImageJ
ij.py.stop()

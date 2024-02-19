import matplotlib.pyplot as plt
from PIL import Image

def click(event):
    """
    Function to handle mouse clicks on the image.

    Args:
        event: The matplotlib event object.
    """
    # Get the coordinates of the clicked point
    x = event.xdata
    y = event.ydata

    # Round the coordinates to the nearest fixel
    x = round(x / fixel_width) * fixel_width
    y = round(y / fixel_height) * fixel_height

    # Add the clicked point to a list
    clicked_points.append((x, y))

    # Draw the fixel at the clicked point
    for i in range(fixel_width):
        for j in range(fixel_height):
            image.putpixel((x + i, y + j), (255, 0, 0))

    # Update the image and plot the clicked points
    ax.imshow(image)
    ax.plot(*zip(*clicked_points), 'o', color='red')
    plt.draw()

# Load the image
image = Image.open('1.png')

# Convert the image to RGB
image = image.convert('RGB')

# Get the image size
image_width, image_height = image.size

# Define the fixel size
fixel_width = 16
fixel_height = 16

# Calculate the number of fixels
fixel_count = (image_width // fixel_width) * (image_height // fixel_height)

# Define a list to store the clicked points
clicked_points = []

# Create the figure and axes
fig, ax = plt.subplots(1)

# Connect the mouse click event to the function
fig.canvas.mpl_connect('button_press_event', click)

# Show the image
ax.imshow(image)
plt.show()

# Calculate the dimensions from fixel count
width = fixel_count * fixel_width
height = fixel_count * fixel_height

print("Width:", width)
print("Height:", height)

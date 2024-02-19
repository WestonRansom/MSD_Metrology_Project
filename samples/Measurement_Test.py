import cv2
import numpy as np

# Global variables
points = []

# Known physical dimension of the image in millimeters
image_width_mm = 250.0  # Replace with the correct value

def calculate_distance(point1, point2):
    # Calculate the distance between two points in pixels
    distance_pixels = np.linalg.norm(np.array(point2) - np.array(point1))
    return distance_pixels

def on_click(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

        if len(points) == 2:
            # Draw a line between the selected points
            cv2.line(image, points[0], points[1], (0, 0, 255), 2)

            # Calculate the distance between the points in millimeters
            distance_mm = (calculate_distance(points[0], points[1]) / image.shape[1]) * image_width_mm

            # Convert to centimeters
            distance_cm = distance_mm / 10.0

            # Print the measured distance in centimeters
            print("Measured distance:", distance_cm, "centimeters")

            # Reset points for the next measurement
            points = []

            cv2.imshow("Image", image)

# Load the image
image = cv2.imread(
    r"C:\Users\westontest\OneDrive - rit.edu\Fifth Year\MSD\WestonCameraTest\tisgrabber\samples\images - Copy\final_merged_image.jpg")

# Create a window and set the mouse callback function
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", on_click)

while True:
    cv2.imshow("Image", image)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

cv2.destroyAllWindows()

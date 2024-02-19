import ctypes
import tisgrabber as tis
import time
import serial.tools.list_ports
import pygetwindow as gw
def initialize_camera():
    try:
        ic = ctypes.cdll.LoadLibrary("./tisgrabber_x64.dll")
        tis.declareFunctions(ic)
        ic.IC_InitLibrary(0)
        hGrabber = tis.openDevice(ic)

        if ic.IC_IsDevValid(hGrabber):
            print("Camera initialized successfully.")
            ic.IC_StartLive(hGrabber, 1)

            windows = gw.getWindowsWithTitle("ActiveMovie Window")
            if windows:
                window = windows[0]
                window.resize(200, 300)
            else:
                print("ActiveMovie Window not found.")

            return ic, hGrabber
        else:
            raise ValueError("Camera not found or device not valid")

    except Exception as e:
        print(f"Error initializing camera: {e}")
        exit()

def capture_image(ic, hGrabber, filename):
    try:
        if ic.IC_SnapImage(hGrabber, 2000) == tis.IC_SUCCESS:
            full_path = r"C:\Users\westontest\OneDrive - rit.edu\Fifth Year\MSD\WestonCameraTest\tisgrabber\samples\images\\" + filename
            ic.IC_SaveImage(hGrabber, tis.T(full_path), tis.ImageFileTypes['JPEG'], 90)
            print(f"Image saved as {full_path}")
            return True
        else:
            print("Error capturing image: No frame received in 2 seconds.")
            return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def move_to_next_location(serial, x_pos, y_pos):
    x_cmd = f'X{x_pos:.3f}'
    y_cmd = f'Y{y_pos:.3f}'
    move_cmd = f'G1 {x_cmd} {y_cmd}\n'
    serial.write(move_cmd.encode())
    response = serial.readline().decode().strip()
    print("Response:", response)
    time.sleep(2)

def move_to_next_locationz(serial, z_pos):
    z_cmd = f'Z{z_pos:.3f}'
    feedrate = f'F{7800:.3f}'
    move_cmd = f'G1 {z_cmd} {feedrate}\n'
    serial.write(move_cmd.encode())
    response = serial.readline().decode().strip()
    print("Response:", response)
    time.sleep(2)

def close_camera(ic, hGrabber):
    ic.IC_StopLive(hGrabber)
    ic.IC_ReleaseGrabber(hGrabber)

def capture_images_and_merge(ic, hGrabber, num_images, serial, x_pos, y_pos):
    filename = f"image_{x_pos}_{y_pos}.jpg"
    capture_image(ic, hGrabber, filename)
    time.sleep(2)
    move_to_next_location(serial, x_pos, y_pos)
    time.sleep(2)

def home_all_axes(serial):
    serial.write(b'G28 X0 Y0\n')  # Home X and Y axes
    time.sleep(1)  # Adjust delay based on printer response time

    serial.write(b'G28 Z0\n')  # Home Z axis
    time.sleep(1)  # Adjust delay based on printer response time

    print("All axes homed.")

# Serial port initialization and movement to initial position
serial = serial.Serial('COM22', 115200)
serial.write(b'G90\n')

#Attempt to home all Axes before begining imaging
#time.sleep(0.1)
#print('Homing all axes...')
#home_all_axes(serial)

#move to the proper location
move_to_next_location(serial, 45, 0)
move_to_next_locationz(serial, 80)

# Camera initialization
ic, hGrabber = initialize_camera()

# Define image dimensions and build plate area
image_width = 54  # Width of the captured image in millimeters
image_height = 100  # Height of the captured image in millimeters

build_plate_width = 260  # Width of the build plate in millimeters
build_plate_height = 260  # Height of the build plate in millimeters

# Calculate the number of steps needed in each direction
num_steps_x = int(build_plate_width / image_width)  # Use int() for integer steps
num_steps_y = int(build_plate_height / image_height)

# Calculate the step size for precise positioning
step_size_x = build_plate_width / num_steps_x
step_size_y = build_plate_height / num_steps_y

for y in range(num_steps_y):
    for x in range(num_steps_x):
        x_pos = x * step_size_x
        y_pos = y * step_size_y

        # Capture and merge images at the current position
        capture_images_and_merge(ic, hGrabber, 1, serial, x_pos, y_pos)  # Capture 1 image at each position

close_camera(ic, hGrabber)




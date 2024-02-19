import os
import ctypes
import tisgrabber as tis
import time
import serial.tools.list_ports
import pygetwindow as gw


def delete_images_in_folder(folder_path):
    try:
        files = os.listdir(folder_path)
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(folder_path, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        print("All images deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def initialize_camera_Test(video_format=None, image_folder=None):
    try:
        # Delete images in the folder before initializing the camera
        delete_images_in_folder(image_folder)
        ic = ctypes.cdll.LoadLibrary("./tisgrabber_x64.dll")
        tis.declareFunctions(ic)
        ic.IC_InitLibrary(0)
        hGrabber = tis.openDevice(ic)
        ic.IC_SetVideoFormat(hGrabber, tis.T(video_format))
        print(f"Video format set to: {video_format}")

        if ic.IC_IsDevValid(hGrabber):
            print("Camera initialized successfully.")
            ic.IC_StartLive(hGrabber, 1)
            return ic, hGrabber
        else:
            raise ValueError("Camera not found or device not valid")

    except Exception as e:
        print(f"Error initializing camera: {e}")
        exit()


def delete_images_in_folder(folder_path):
    try:
        files = os.listdir(folder_path)
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(folder_path, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        print("All images deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def capture_image_after_pause(ic, hGrabber, filename):
    try:
        time.sleep(2)
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


def move_to_next_location_with_capture(ic, hGrabber, serial, gcode_command, image_counter):
    serial.write(gcode_command.encode())
    response = serial.readline().decode().strip()
    print("Response:", response)
    time.sleep(2)
    capture_image_after_pause(ic, hGrabber, f"image_{image_counter}.jpg")



def close_camera(ic, hGrabber):
    ic.IC_StopLive(hGrabber)
    ic.IC_ReleaseGrabber(hGrabber)


# Serial port initialization and movement to initial position
serial = serial.Serial('COM25', 115200)
serial.write(b'G90\n')

# Camera initialization
custom_video_format = "Y800 (1024x768)"
image_folder = r"C:\Users\westontest\OneDrive - rit.edu\Fifth Year\MSD\WestonCameraTest\tisgrabber\samples\images\\"
ic, hGrabber = initialize_camera_Test(video_format=custom_video_format, image_folder=image_folder)

# Execute the G-code commands one by one
image_counter = 1

#gcode_commands = ['G10 P0 L20 X0 Y0 Z0\n']

gcode_commands = [
'G90 X0 Y0 Z0\n',
'G90 X0 Y62\n',
'G90 X0 Y124\n',
'G90 X0 Y186\n',
'G90 X0 Y248\n',
'G90 X0 Y310\n',
'G90 Z62\n',
'G90 X0 Y248\n',
'G90 X0 Y186\n',
'G90 X0 Y124\n',
'G90 X0 Y62\n',
'G90 X0 Y0\n',
'G90 Z124\n',
'G90 X0 Y62\n',
'G90 X0 Y124\n',
'G90 X0 Y186\n',
'G90 X0 Y248\n',
'G90 X0 Y310\n',
'G90 Z186\n',
'G90 X0 Y248\n',
'G90 X0 Y186\n',
'G90 X0 Y124\n',
'G90 X0 Y62\n',
'G90 X0 Y0\n',
'G90 Z248\n',
'G90 X0 Y62\n',
'G90 X0 Y124\n',
'G90 X0 Y186\n',
'G90 X0 Y248\n',
'G90 X0 Y310\n',
'G90 Z310\n',
'G90 X0 Y248\n',
'G90 X0 Y186\n',
'G90 X0 Y124\n',
'G90 X0 Y62\n',
'G90 X0 Y0\n',
'G90 X0 Y0 Z0\n',
]

for gcode_command in gcode_commands:
    move_to_next_location_with_capture(ic, hGrabber, serial, gcode_command, image_counter)
    image_counter += 1

# Close Camera
close_camera(ic, hGrabber)
ic.IC_ReleaseGrabber(hGrabber)

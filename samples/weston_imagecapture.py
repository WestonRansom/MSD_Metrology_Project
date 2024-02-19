import ctypes
import tisgrabber as tis
import time
import serial.tools.list_ports
import pygetwindow as gw  # Import pygetwindow

def initialize_camera(width, height):
    try:
        ic = ctypes.cdll.LoadLibrary("./tisgrabber_x64.dll")
        tis.declareFunctions(ic)
        ic.IC_InitLibrary(0)
        hGrabber = ic.IC_ShowDeviceSelectionDialog(None)

        if ic.IC_IsDevValid(hGrabber):
            print("Camera initialized successfully.")
            ic.IC_SetVideoFormat(hGrabber, width, height, 60)  # Set the desired resolution here
            ic.IC_StartLive(hGrabber, 1)  # Start live mode

            # Find and resize the ActiveMode window if it exists
            windows = gw.getWindowsWithTitle("ActiveMovie Window")
            if windows:
                window = windows[0]
                window.resize(200, 300)  # Change the dimensions as needed
            else:
                print("ActiveMovie Window not found.")

            return ic, hGrabber
        else:
            raise ValueError("Camera not found or device not valid")

    except Exception as e:
        print(f"Error initializing camera: {e}")
        exit()

def capture_images(ic, hGrabber, serial, build_plate_width, build_plate_height, image_width, image_height):
    try:
        # Calculate the number of steps needed in each direction
        num_steps_x = int(build_plate_width / image_width)
        num_steps_y = int(build_plate_height / image_height)

        # Calculate the step size for precise positioning
        step_size_x = build_plate_width / num_steps_x
        step_size_y = build_plate_height / num_steps_y

        serial.write(b'G90\n')
        time.sleep(0.1)

        for y in range(num_steps_y):
            for x in range(num_steps_x):
                x_pos = x * step_size_x
                y_pos = y * step_size_y

                filename = f"image_{x_pos}_{y_pos}.jpg"
                full_path = r"C:\Users\westontest\OneDrive - rit.edu\Fifth Year\MSD\WestonCameraTest\tisgrabber\samples\images\\" + filename

                ic.IC_SnapImage(hGrabber, 2000)
                ic.IC_SaveImage(hGrabber, tis.T(full_path), tis.ImageFileTypes['JPEG'], 90)

                # Move to the next location with specified x and y coordinates
                x_cmd = f'X{x_pos:.3f}'
                y_cmd = f'Y{y_pos:.3f}'
                move_cmd = f'G1 {x_cmd} {y_cmd}\n'
                serial.write(move_cmd.encode())
                response = serial.readline().decode().strip()
                print("Response:", response)
                time.sleep(2)

        ic.IC_StopLive(hGrabber)
        ic.IC_ReleaseGrabber(hGrabber)

    except Exception as e:
        print(f"Error capturing images: {e}")

# Main execution
image_width = 1280  # Width of the captured image in pixels
image_height = 720  # Height of the captured image in pixels

build_plate_width = 250  # Width of the build plate in millimeters
build_plate_height = 250  # Height of the build plate in millimeters

serial = serial.Serial('COM24', 115200)
ic, hGrabber = initialize_camera(image_width, image_height)

capture_images(ic, hGrabber, serial, build_plate_width, build_plate_height, image_width, image_height)

import win32gui
import pyautogui
import pydirectinput

def get_focus():
    program_name = 'EverQuest'
    handle = win32gui.FindWindow(None, program_name)

    if handle != 0:
        # If the application is minimized, show the window with it's last used placement and dimensions
        if win32gui.IsIconic(handle):
            #print("Application is minimized...")
            win32gui.ShowWindow(handle, 1)

        #print(f"Activating window '{program_name}'...")
        win32gui.SetForegroundWindow(handle)

    else:
        print(f"The program {program_name} could not be found!")


def send_key(key_name):
    # Need to figure out DirectInput key codes

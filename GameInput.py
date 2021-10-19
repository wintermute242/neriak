import win32gui
import pyautogui
import pydirectinput
import time

def get_focus():
    program_name = 'EverQuest'
    handle = win32gui.FindWindow(None, program_name)

    if handle != 0:
        # If the application is minimized, show the window with it's last used placement and dimensions
        if win32gui.IsIconic(handle):
            print("Application is minimized...")
            win32gui.ShowWindow(handle, 1)

        print(f"Activating window '{program_name}'...")
        win32gui.SetForegroundWindow(handle)
        time.sleep(0.05) # Give the window enough time to get focus or the keystroke will go who knows where

    else:
        print(f"The program {program_name} could not be found!")


def send(key_value):
    keys = key_value.split('+')

    if len(keys) > 1:
        send_key_combination(keys)
    
    else:
        send_key(keys[0])


def send_key(key_name):
    print("send_key")
    # DirectInput Key Codes 
    # at https://github.com/learncodebygaming/pydirectinput/blob/master/pydirectinput/__init__.py
    get_focus()
    pydirectinput.press(key_name)


def send_key_combination(*keys):
    print("send_key_combination")
    get_focus()
    for key in keys:
        pydirectinput.keyDown(key)

    for key in keys:
        pydirectinput.keyUp(key)
    
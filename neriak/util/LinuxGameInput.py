import subprocess
import time

# Had to add delay to keydown so when you stop follow it holds the button down long enough
def _press_key(key_name):
    #subprocess.run(["xdotool", "keydown", key_name])
    #subprocess.run(["sleep", "0.01"])
    #subprocess.run(["xdotool", "keyup", key_name])
    subprocess.run(f"xdotool keydown {key_name}; sleep 0.01; xdotool keyup {key_name}", shell=True)


def _focus_window(window_id):
    # Activate the window using xdotool
    subprocess.run(["xdotool", "windowactivate", window_id])


def _is_window_in_background(window_id):
    # Get the window ID of the currently focused window
    focused_window_id = subprocess.check_output(["xdotool", "getwindowfocus"]).decode().strip()

    # Compare the focused window ID with the given window ID
    if window_id == focused_window_id:
        return False  # Window is in the foreground (focused)
    else:
        return True  # Window is in the background


def get_focus():
    window_id = subprocess.check_output(["xdotool", "search", "--name", "EverQuest"]).decode().strip()
    if _is_window_in_background(window_id):
        print("Application is minimized...")
        _focus_window(window_id)
        time.sleep(0.25) # Give the window enough time to get focus or the keystroke will go who knows where
    
    else:
        pass
        #print(f"Activating window '{program_name}'..."


def send_key(key_name):
    print('send_key')
    get_focus()
    # Clear any existing modifiers (e.g., Shift, Ctrl)
    subprocess.run(["xdotool", "keyup", "--clearmodifiers"])
    _press_key(key_name)


# Untested and haven't touched much yet. Work on it tomorrow I guess.
def send_key_combination(keys):
    print(f"send_key_combination {keys}")
    get_focus()
    for key in keys:
        subprocess.run(["xdotool", "key"] + keys)
    for key in keys:
        subprocess.run(["xdotool", "keydown", key])
        subprocess.run(["sleep", "0.01"])

    for key in keys:
        subprocess.run(["xdotool", "keyup", key])
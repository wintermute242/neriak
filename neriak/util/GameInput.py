import sys
if sys.platform.startswith('win'):
    from neriak.util import WindowsGameInput as Input
elif sys.platform.startswith('linux'):
    from neriak.util import LinuxGameInput as Input

import time


def get_focus() -> None:
    Input.get_focus()


def send(key_value: str) -> None:
    if key_value:
        # The '+' character is reserved for splitting key combinations
        keys = key_value.split('+')

        if len(keys) > 1:
            send_key_combination(keys)

        else:
            send_key(keys[0])


def send_key(key_name: str) -> None:
    Input.send_key(key_name)


def send_key_combination(keys: str) -> None:
    Input.send_key_combination(keys)


def pause(seconds: int) -> None:
    """Pauses execution for specified number of seconds. This can be a float for fractions of a second."""
    time.sleep(seconds)
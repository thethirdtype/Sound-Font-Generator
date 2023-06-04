import tkinter as tk
from tkinter import filedialog
import os
import SoundBender


def browse_file(event=None):
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path = convert_path(file_path)
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)


def browse_output_folder(event=None):
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path = convert_path(folder_path)
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(tk.END, folder_path)


def center_window():
    # Update the window to ensure it's rendered on the screen
    window.update()

    # Get the screen resolution
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Set the window position
    x_position = int((screen_width - window.winfo_width()) / 2)
    y_position = int((screen_height - window.winfo_height()) / 2)

    # Set the window geometry
    window.geometry(f"{window.winfo_width()}x{window.winfo_height()}+{x_position}+{y_position}")


def close_form(event=None):
    window.destroy()


def convert_path(path):
    if os.name == 'nt':  # Check if running on Windows
        path = path.replace('/', '\\')  # Convert forward slashes to backslashes
    return path


def start_processing(event=None):
    # Get the selected options from widgets
    input_file = input_entry.get()
    reverse = reverse_var.get()
    pitch_adjustment = int(pitch_adjustment_entry.get())
    pitch_divisions = int(pitch_divisions_entry.get())
    pitch_direction = pitch_direction_var.get()
    output_prefix = output_prefix_entry.get()
    output_folder = output_folder_entry.get()
    reverse_order = reverse_order_var.get()

    # Validate input file
    if not os.path.isfile(input_file):
        status_label.config(text='Error: Invalid input file.')
        return

    # Call the library function
    SoundBender.process_audio_file(
        input_file=input_file,
        reverse=reverse,
        pitch_adjustment=pitch_adjustment,
        pitch_divisions=pitch_divisions,
        pitch_direction=pitch_direction,
        output_prefix=output_prefix,
        output_folder=output_folder,
        reverse_order=reverse_order
    )

    status_label.config(text='Audio processing completed successfully.')


# Create the main window
window = tk.Tk()
window.title('Sound Bender')

# Set padding for all widgets
padding = 10

# Input file label, entry, and browse button
input_label = tk.Label(window, text='Input File:')
input_label.grid(row=0, column=0, sticky=tk.E, padx=padding, pady=padding)
input_entry = tk.Entry(window)
input_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
browse_button = tk.Button(window, text='Browse', command=browse_file)
browse_button.grid(row=0, column=3, sticky=tk.W, padx=padding, pady=padding)
browse_button.bind("<Return>", browse_file)

# Pitch adjustment label and entry
pitch_adjustment_label = tk.Label(window, text='Pitch Adjustment:')
pitch_adjustment_label.grid(row=1, column=0, sticky=tk.E, padx=padding, pady=padding)
pitch_adjustment_entry = tk.Entry(window)
pitch_adjustment_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
pitch_adjustment_entry.insert(tk.END, '0')

# Pitch divisions label and entry
pitch_divisions_label = tk.Label(window, text='Pitch Divisions:')
pitch_divisions_label.grid(row=2, column=0, sticky=tk.E, padx=padding, pady=padding)
pitch_divisions_entry = tk.Entry(window)
pitch_divisions_entry.grid(row=2, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
pitch_divisions_entry.insert(tk.END, '1')

# Pitch direction radio buttons
pitch_direction_var = tk.StringVar(value='up')
pitch_direction_label = tk.Label(window, text='Pitch Direction:')
pitch_direction_label.grid(row=3, column=0, sticky=tk.E, padx=padding, pady=padding)
up_radio = tk.Radiobutton(window, text='Up', variable=pitch_direction_var, value='up')
up_radio.grid(row=3, column=1, sticky=tk.W, padx=padding, pady=padding)
down_radio = tk.Radiobutton(window, text='Down', variable=pitch_direction_var, value='down')
down_radio.grid(row=3, column=2, sticky=tk.E, padx=padding, pady=padding)

# Output prefix label and entry
output_prefix_label = tk.Label(window, text='Output Prefix:')
output_prefix_label.grid(row=4, column=0, sticky=tk.E, padx=padding, pady=padding)
output_prefix_entry = tk.Entry(window)
output_prefix_entry.grid(row=4, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)

# Output folder label, entry, and browse button
output_folder_label = tk.Label(window, text='Output Folder:')
output_folder_label.grid(row=5, column=0, sticky=tk.E, padx=padding, pady=padding)
output_folder_entry = tk.Entry(window)
output_folder_entry.grid(row=5, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
output_browse_button = tk.Button(window, text='Browse', command=browse_output_folder)
output_browse_button.grid(row=5, column=3, sticky=tk.W, padx=padding, pady=padding)
output_browse_button.bind("<Return>", browse_output_folder)

# Reverse checkboxes
reverse_label = tk.Label(window, text='Reverse:')
reverse_label.grid(row=6, column=0, sticky=tk.E, padx=padding, pady=padding)
reverse_var = tk.BooleanVar()
reverse_check = tk.Checkbutton(window, text='Audio Output', variable=reverse_var)
reverse_check.grid(row=6, column=1, sticky=tk.W, padx=padding, pady=padding)
reverse_order_var = tk.BooleanVar()
reverse_order_check = tk.Checkbutton(window, text='File Order', variable=reverse_order_var)
reverse_order_check.grid(row=6, column=2, sticky=tk.E, padx=padding, pady=padding)

# Close and Start buttons
close_button = tk.Button(window, text='Close', command=close_form)
close_button.grid(row=7, column=0, columnspan=2, pady=padding)
close_button.bind("<Return>", close_form)
start_button = tk.Button(window, text='Start', command=start_processing)
start_button.grid(row=7, column=1, columnspan=3, pady=padding)
start_button.bind("<Return>", start_processing)

# Status label
status_label = tk.Label(window, text='')
status_label.grid(row=8, column=0, columnspan=4, pady=padding)

# Configure grid weights to make widgets resize when form is resized
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)
window.grid_rowconfigure(8, weight=1)

# Send titlebar close to close_form function
window.protocol("WM_DELETE_WINDOW", close_form)

# Place window center screen
center_window()

# Start the main loop
window.mainloop()

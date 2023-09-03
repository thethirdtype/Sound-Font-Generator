import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import random
import os
import SoundFont


def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path = convert_path(file_path)
        input_entry.delete(0, tk.END)
        input_entry.insert(tk.END, file_path)


def browse_output_folder():
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
    if os.name == "nt":  # Check if running on Windows
        path = path.replace("/", "\\")  # Convert forward slashes to backslashes
    return path


def create_sound_font(event=None):
    config_file = input_entry.get()
    output_folder = output_folder_entry.get()
    project_name = project_name_entry.get()
    author_name = author_name_entry.get()
    blade_color = blade_color_entry.get()

    # Extract the integer portion from the combobox options
    light_effect = int(light_effect_combo.get().split()[0])
    blade_style = int(blade_style_combo.get().split()[0])

    on_speed = int(on_speed_entry.get())
    off_speed = int(off_speed_entry.get())

    # Call the library function
    SoundFont.create_font(config_file, output_folder, project_name, author_name,
                          blade_color, light_effect, blade_style, on_speed, off_speed)

    status_label.config(text="Sound font generation successful.")


def get_random_color():
    # List of colors to choose from, all unique values from stock xenopixel v2
    color_choices = ["#0000FF", "#FFFF00", "#FFFFFF", "#FF0000", "#FF33FF", "#00FFFF", "#9632FF", "#FF8000",
                     "#00FF00", "#AF00FF", "#CC80FF", "#80FF80", "#32A0FF", "#FF00FF", "#FF9912", "#FFC0CB"]

    # Randomly select a color from the list
    default_color = random.choice(color_choices)

    # Convert hexadecimal color to RGB
    r, g, b = [int(default_color[i:i + 2], 16) for i in (1, 3, 5)]

    return default_color, r, g, b


def select_color(event):
    color = colorchooser.askcolor()[1]  # Get the hexadecimal color value
    if color:
        r, g, b = [int(color[i:i+2], 16) for i in (1, 3, 5)]  # Convert hex to decimal
        blade_color_entry.delete(0, tk.END)
        blade_color_entry.insert(tk.END, f"{r}, {g}, {b}")
        color_rectangle.configure(bg=color)
        window.update()  # Update the window to reflect the color change


def update_color(event):
    color_input = blade_color_entry.get()
    try:
        if color_input.startswith("#"):
            # Hexadecimal color input
            r, g, b = [int(color_input[i:i + 2], 16) for i in (1, 3, 5)]
        else:
            # RGB color input
            r, g, b = [int(x.strip()) for x in color_input.split(",")]

        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            color = f"#{r:02x}{g:02x}{b:02x}"  # Convert decimal RGB to hexadecimal
            blade_color_entry.delete(0, tk.END)
            blade_color_entry.insert(tk.END, f"{r}, {g}, {b}")
            color_rectangle.configure(bg=color)
            window.update()  # Update the window to reflect the color change
    except ValueError:
        pass  # Invalid RGB input, do nothing


# Create the main window
window = tk.Tk()
window.title("Sound Font Generator")

# Hide window
window.withdraw()

# Set padding for all widgets
padding = 10

# Input file label, entry, and browse button
input_label = tk.Label(window, text="Input File:")
input_label.grid(row=0, column=0, sticky=tk.E, padx=padding, pady=padding)
input_entry = tk.Entry(window)
input_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
input_entry.bind("<Enter>", lambda event: status_label.config(text="Enter file location"))
input_entry.bind("<Leave>", lambda event: status_label.config(text=""))
browse_button = tk.Button(window, text="Browse", command=browse_file)
browse_button.grid(row=0, column=3, sticky=tk.W, padx=padding, pady=padding)
browse_button.bind("<Return>", browse_file)
browse_button.bind("<Enter>", lambda event: status_label.config(text="Browse to file location"))
browse_button.bind("<Leave>", lambda event: status_label.config(text=""))

# Output folder label, entry, and browse button
output_folder_label = tk.Label(window, text="Output Folder:")
output_folder_label.grid(row=1, column=0, sticky=tk.E, padx=padding, pady=padding)
output_folder_entry = tk.Entry(window)
output_folder_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
output_folder_entry.bind("<Enter>", lambda event: status_label.config(text="Enter folder location"))
output_folder_entry.bind("<Leave>", lambda event: status_label.config(text=""))
output_folder_button = tk.Button(window, text="Browse", command=browse_output_folder)
output_folder_button.grid(row=1, column=3, sticky=tk.W, padx=padding, pady=padding)
output_folder_button.bind("<Return>", browse_output_folder)
output_folder_button.bind("<Enter>", lambda event: status_label.config(text="Browse to folder location"))
output_folder_button.bind("<Leave>", lambda event: status_label.config(text=""))

# Project name label and entry
project_name_label = tk.Label(window, text="Project Name:")
project_name_label.grid(row=2, column=0, sticky=tk.E, padx=padding, pady=padding)
project_name_entry = tk.Entry(window)
project_name_entry.grid(row=2, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
project_name_entry.bind("<Enter>", lambda event: status_label.config(text="Input project name for project's .txt file"))
project_name_entry.bind("<Leave>", lambda event: status_label.config(text=""))

# Author name label and entry
author_name_label = tk.Label(window, text="Author Name:")
author_name_label.grid(row=3, column=0, sticky=tk.E, padx=padding, pady=padding)
author_name_entry = tk.Entry(window)
author_name_entry.grid(row=3, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
author_name_entry.bind("<Enter>", lambda event: status_label.config(text="Input author name for project's .txt file"))
author_name_entry.bind("<Leave>", lambda event: status_label.config(text=""))

# Blade color label, entry, rectangle
default_color, r, g, b = get_random_color()  # Get a random color
blade_color_label = tk.Label(window, text="Blade Color:")
blade_color_label.grid(row=4, column=0, sticky=tk.E, padx=padding, pady=padding)
blade_color_entry = tk.Entry(window)
blade_color_entry.insert(tk.END, f"{r}, {g}, {b}")  # Set RGB values as default
blade_color_entry.grid(row=4, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
blade_color_entry.bind("<Return>", update_color)
blade_color_entry.bind("<Enter>", lambda event: status_label.config(text="Input R, G, B or Hex value"))
blade_color_entry.bind("<Leave>", lambda event: status_label.config(text=""))
color_rectangle = tk.Label(window, width=10, height=2)
color_rectangle.grid(row=4, column=3, padx=padding, sticky=tk.W, pady=padding)
color_rectangle.bind("<Button-1>", select_color)
color_rectangle.configure(bg=default_color, width=6, height=1)  # Default color and WxH
color_rectangle.bind("<Enter>", lambda event: status_label.config(text="Click to open color palette"))
color_rectangle.bind("<Leave>", lambda event: status_label.config(text=""))

# Light effect label and combo box
light_effect_label = tk.Label(window, text="Light Effect:")
light_effect_label.grid(row=5, column=0, sticky=tk.E, padx=padding, pady=padding)
light_effect_combo = tk.StringVar()
light_effect_combo.set("1 Steady")
light_effect_choices = ["0 Fire", "1 Steady", "2 Pulse", "3 Rainbow", "4 Candy", "5 Unstable", "6 Crack"]
light_effect_dropdown = tk.OptionMenu(window, light_effect_combo, *light_effect_choices)
light_effect_dropdown.grid(row=5, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
light_effect_dropdown.bind("<Enter>", lambda event: status_label.config(text="Choose light effect"))
light_effect_dropdown.bind("<Leave>", lambda event: status_label.config(text=""))

# Blade style label and combo box
blade_style_label = tk.Label(window, text="Blade Style:")
blade_style_label.grid(row=6, column=0, sticky=tk.E, padx=padding, pady=padding)
blade_style_combo = tk.StringVar()
blade_style_combo.set("0 Standard")
blade_style_choices = ["0 Standard", "1 Blaster", "2 Ghost", "3 Broken", "4 Warp",
                       "5 Stack", "6 Phaser", "7 Photon", "8 Scavenger", "9 Hunter"]
blade_style_dropdown = tk.OptionMenu(window, blade_style_combo, *blade_style_choices)
blade_style_dropdown.grid(row=6, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
blade_style_dropdown.bind("<Enter>", lambda event: status_label.config(text="Choose blade style"))
blade_style_dropdown.bind("<Leave>", lambda event: status_label.config(text=""))

# On speed label and entry
on_speed_label = tk.Label(window, text="On Speed:")
on_speed_label.grid(row=7, column=0, sticky=tk.E, padx=padding, pady=padding)
on_speed_entry = tk.Entry(window)
on_speed_entry.grid(row=7, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
on_speed_entry.insert(tk.END, "300")  # Xenopixel v2 stock: 750 avg, 300 median
on_speed_entry.bind("<Enter>", lambda event: status_label.config(text="Input on speed"))
on_speed_entry.bind("<Leave>", lambda event: status_label.config(text=""))

# Off speed label and entry
off_speed_label = tk.Label(window, text="Off Speed:")
off_speed_label.grid(row=8, column=0, sticky=tk.E, padx=padding, pady=padding)
off_speed_entry = tk.Entry(window)
off_speed_entry.grid(row=8, column=1, columnspan=2, sticky=tk.W+tk.E, padx=padding, pady=padding)
off_speed_entry.insert(tk.END, "700")  # Xenopixel v2 stock: 1037.5 avg, 700 median
off_speed_entry.bind("<Enter>", lambda event: status_label.config(text="Input off speed"))
off_speed_entry.bind("<Leave>", lambda event: status_label.config(text=""))

# Close and Generate buttons
close_button = tk.Button(window, text="Close", command=close_form)
close_button.grid(row=9, column=0, columnspan=2, pady=padding)
close_button.bind("<Return>", close_form)
close_button.bind("<Enter>", lambda event: status_label.config(text="Close window"))
close_button.bind("<Leave>", lambda event: status_label.config(text=""))
generate_button = tk.Button(window, text="Generate", command=create_sound_font)
generate_button.grid(row=9, column=1, columnspan=3, pady=padding)
generate_button.bind("<Return>", create_sound_font)
generate_button.bind("<Enter>", lambda event: status_label.config(text="Generate sound font"))
generate_button.bind("<Leave>", lambda event: status_label.config(text=""))

# Status label
status_label = tk.Label(window, text="")
status_label.grid(row=10, column=0, columnspan=4, pady=padding)

# Configure grid to resize with the window
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

# Send titlebar close to close_form function
window.protocol("WM_DELETE_WINDOW", close_form)

# Place window center screen
center_window()

# Show window
window.deiconify()

# Set Icon
window.iconbitmap("sfg_icon.ico")

# Start the main loop
window.mainloop()

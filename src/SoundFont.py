import argparse
import datetime
import os
import configparser


r'''
To use this app, run it from the command line with the required arguments. For example:

Linux:
python SoundFont.py --config_file config.ini --output_folder /sounds --project_name "Buzz" 
--author_name "Bees" --blade_color "(255,0,0)" --light_effect 1 --blade_style 0 --on_speed 300 --off_speed 800

Windows:
python SoundFont.py --config_file "D:\set\config.ini" --output_folder "C:\sounds" --project_name "Buzz" 
--author_name "Bees" --blade_color "(255,0,0)" --light_effect 1 --blade_style 0 --on_speed 300 --off_speed 800

This will add an entry for a red saber into config.ini with a steady blade (light_effect 1), standard blade style 
(blade_style 0), on speed of 300, off speed of 800, and it also creates a Project file named "Buzz.txt" under the sounds 
folder, including the author name "Bees" and current date.
'''


def create_config_file(config_file):
    with open(config_file, "w"):
        pass


def parse_config_file(config_file):
    if not os.path.exists(config_file):
        create_config_file(config_file)
        next_color_entry = 1
        found_line = 0
    else:
        with open(config_file, "r") as file:
            lines = file.readlines()
        found_line = len(lines) - 1
        next_color_entry = 1
        for i, line in enumerate(lines):
            if line.startswith("Color-"):
                found_line = i
                number = int(line.split("=")[0].split("-")[1])
                next_color_entry = number + 1
    return next_color_entry, found_line


def generate_output_string(blade_color, light_effect, on_speed, off_speed, blade_style, next_color_entry):
    # Remove parentheses if present
    blade_color = blade_color.strip("()")

    # Remove spaces from the blade color string
    blade_color = blade_color.replace(" ", "")

    # Split the color components
    color_components = blade_color.split(",")

    # Check if there are exactly three color components
    if len(color_components) != 3:
        raise ValueError("Blade color must have exactly three numerical values.")

    # Check if each color component is a valid numerical value in the range of 0 to 255
    for component in color_components:
        if not component.isdigit() or not 0 <= int(component) <= 255:
            raise ValueError("Invalid blade color. Each color component must be a numerical value between 0 and 255.")

    # Concatenate the color components and other parameters to form the output string
    output_string = f"Color-{next_color_entry}=({blade_color}),{light_effect},{on_speed},{off_speed},{blade_style}\n"

    return output_string


def write_output_string_to_config_file(output_string, config_file, found_line):
    with open(config_file, "r") as file:
        lines = file.readlines()

    lines.insert(found_line + 1, output_string)

    with open(config_file, "w") as file:
        file.writelines(lines)


def create_project_file(output_folder, project_name, author_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not project_name:
        return
    file_name = os.path.join(output_folder, f"{project_name}.txt")
    author_str = f" © {author_name}" if author_name else ""
    date_str = datetime.date.today().strftime("%d %B %Y")
    content = f"“{project_name}”{author_str} {date_str}."
    with open(file_name, "w") as file:
        file.write(content)


def create_font(config_file, output_folder, project_name, author_name, blade_color,
                light_effect, blade_style, on_speed, off_speed):
    try:
        next_color_entry, found_line = parse_config_file(config_file)
        output_string = generate_output_string(blade_color, light_effect, on_speed,
                                               off_speed, blade_style, next_color_entry)
        write_output_string_to_config_file(output_string, config_file, found_line)

        create_project_file(output_folder, project_name, author_name)

        print("Sound font generation successful.")
    except Exception as e:
        print("Error:", str(e))


def main():
    parser = argparse.ArgumentParser(description="Sound Font Generator")
    parser.add_argument("--config_file", type=str, help="Config File")
    parser.add_argument("--output_folder", type=str, help="Output Folder")
    parser.add_argument("--project_name", type=str, help="Project Name")
    parser.add_argument("--author_name", type=str, help="Author Name")
    parser.add_argument("--blade_color", type=str, required=True, help="Blade Color")
    parser.add_argument("--light_effect", type=int, required=True, help="Light Effect")
    parser.add_argument("--blade_style", type=int, required=True, help="Blade Style")
    parser.add_argument("--on_speed", type=int, required=True, help="On Speed")
    parser.add_argument("--off_speed", type=int, required=True, help="Off Speed")
    args = parser.parse_args()

    create_font(args.config_file, args.output_folder, args.project_name, args.author_name,
                args.blade_color, args.light_effect, args.blade_style, args.on_speed, args.off_speed)


if __name__ == "__main__":
    main()

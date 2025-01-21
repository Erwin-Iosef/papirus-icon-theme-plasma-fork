import os
from bs4 import BeautifulSoup

# Path to the directory containing SVG files
directory = '/path/to/your/svg/files'

# Style element to be added
style_element = '''<style type="text/css" id="current-color-scheme">
   .ColorScheme-Text {
     color:#232629;
   }
   </style>'''

# Ensure the directory exists
if not os.path.isdir(directory):
    raise ValueError(f"Directory {directory} does not exist")

def modify_svg(filepath, visited_symlinks=set()):
    """Modify and clean up the SVG file by adding a style element and class attribute."""
    try:
        # Avoid circular symlinks
        if filepath in visited_symlinks:
            print(f"Skipping circular symlink: {filepath}")
            return
        visited_symlinks.add(filepath)
        
        # Read the SVG file
        with open(filepath, 'r', encoding='utf-8') as file:
            svg_content = file.read()

        # Parse the SVG content
        soup = BeautifulSoup(svg_content, 'xml')

        # Check if the file already has the necessary modifications
        style_element_present = soup.find('style', {'id': 'current-color-scheme'}) is not None
        all_paths_modified = all(
            'fill:currentColor' in path.get('style', '') and 'ColorScheme-Text' in path.get('class', '')
            for path in soup.find_all('path')
        )

        # If everything is already in place, skip the file
        if style_element_present and all_paths_modified:
            print(f"{os.path.basename(filepath)} already has all the modifications, skipping.")
            return

        # Add the style element if not present
        if not style_element_present:
            soup.svg.insert(1, BeautifulSoup(style_element, 'xml'))

        # Update all path elements
        path_elements = soup.find_all('path')
        for path_element in path_elements:
            if 'style' in path_element.attrs:
                path_element['style'] = path_element['style'].replace('fill:#444444', 'fill:currentColor')
            if 'd' in path_element.attrs:
                # Add or update the class attribute
                classes = path_element.get('class', '').split()
                if 'ColorScheme-Text' not in classes:
                    classes.append('ColorScheme-Text')
                path_element['class'] = ' '.join(classes)

        # Write the modified SVG content back to the file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        print(f"Modified {os.path.basename(filepath)} successfully!")

    except Exception as e:
        print(f"Failed to modify {os.path.basename(filepath)}: {e}")

def process_directory(directory, visited_symlinks=set()):
    """Process all SVG files in the directory and its subdirectories."""
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            if filename.endswith('.svg') or (os.path.islink(filepath) and os.readlink(filepath).endswith('.svg')):
                # Handle symlinks by modifying the target file
                if os.path.islink(filepath):
                    target_path = os.path.abspath(os.readlink(filepath))
                    modify_svg(target_path, visited_symlinks)
                else:
                    modify_svg(filepath, visited_symlinks)

# Process the directory recursively
process_directory(directory)

print('All SVG files have been processed!')

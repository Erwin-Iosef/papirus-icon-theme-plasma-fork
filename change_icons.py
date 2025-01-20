import os
from bs4 import BeautifulSoup

# Path to the directory containing SVG files
directory = 'path/to/your/icons/'

# Style element to be added
style_element = '''<style type="text/css" id="current-color-scheme">
   .ColorScheme-Text {
     color:#232629;
   }
   </style>'''

# Ensure the directory exists
if not os.path.isdir(directory):
    raise ValueError(f"Directory {directory} does not exist")

def modify_svg(filepath, visited_symlinks=None):
    """Modify the SVG file by adding a style element and class attribute."""
    if visited_symlinks is None:
        visited_symlinks = set()
    
    # Avoid circular symlinks
    if filepath in visited_symlinks:
        print(f"Skipping circular symlink: {filepath}")
        return
    visited_symlinks.add(filepath)
    
    try:
        # Read and parse the SVG file
        with open(filepath, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'xml')

        # Check for existing modifications
        style_element_present = soup.find('style', {'id': 'current-color-scheme'}) is not None
        all_paths_modified = all(
            'fill:currentColor' in path.get('style', '') and 'ColorScheme-Text' in path.get('class', '').split()
            for path in soup.find_all('path')
        )

        if style_element_present and all_paths_modified:
            print(f"{os.path.basename(filepath)} already has all the modifications, skipping.")
            return

        # Add the style element if not present
        if not style_element_present:
            soup.svg.insert(1, BeautifulSoup(style_element, 'xml'))

        # Update all path elements
        for path_element in soup.find_all('path'):
            if 'style' in path_element.attrs:
                path_element['style'] = path_element['style'].replace('fill:#444444', 'fill:currentColor')
            
            # Add or update the class attribute, remove 'error' if present
            classes = set(path_element.get('class', '').split())
            classes.discard('error')
            classes.add('ColorScheme-Text')
            path_element['class'] = ' '.join(classes)

        # Write the modified SVG content back to the file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        print(f"Modified {os.path.basename(filepath)} successfully!")

    except Exception as e:
        print(f"Failed to modify {os.path.basename(filepath)}: {e}")

def process_directory(directory):
    """Process all SVG files in the directory and its subdirectories."""
    visited_symlinks = set()
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            if filename.endswith('.svg'):
                if os.path.islink(filepath):
                    target_path = os.path.abspath(os.readlink(filepath))
                    modify_svg(target_path, visited_symlinks)
                else:
                    modify_svg(filepath, visited_symlinks)

process_directory(directory)

print('All SVG files have been processed!')

"""
A module to sanitize a Notion output by removing all trailing IDs in titles.
"""

import os
import sys
import zipfile

def rename_path(path_to_rename):
    """
    Renames a given path by removing trailing IDs.

    :param path_to_rename: path-like to file or folder
    """
    # Isolate the file extension if there is any
    if '.' in path_to_rename:
        path_ext = '.' + path_to_rename.split('.')[-1]
    else:
        path_ext = ''

    # If the path contains at least a space, split it and remove the last bit
    if ' ' in path_to_rename:
        split_name = path_to_rename.split(' ')
        renamed_path = ' '.join(split_name[:len(split_name)-1])
        return f'{renamed_path}{path_ext}'
    return path_to_rename

if __name__ == '__main__':
    args = sys.argv

    # Define arguments which can be catched
    source_zip = None

    # Validate inputs
    if len(args) <= 1:
        # No argument found: close the app
        print(
            '[ERROR] No arguments. Please provide the name of the ZIP file '
            'you downloaded from Notion.so in order for the script to run.')
        sys.exit()
    else:
        # Arguments found: check it's a zip file name and it is valid
        source_zip = args[1]
        if not source_zip.endswith('.zip') or not os.path.exists(source_zip):
            print(
                f'[ERROR] Sorry, "{source_zip}" doesn\'t exists. '
                'Refer to the README.md file if you need assistance.'
            )
            sys.exit()

    print('[INFO] Starting the Notion Sanitizer...')

    # Starts by extracting the zip file's content in the data/ folder
    with zipfile.ZipFile(source_zip, 'r') as zipf:
        zipf.extractall('data/')

    # First, we need to iterate over all folders and files to prepare the renamed structure
    folder_dict = {}
    files_dict = {}
    for (root, dirs, files) in os.walk('data', topdown=False):
        # Remove trailing IDs from folder names and cache them
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            renamed_folder_path = rename_path(folder_path)
            new_folder_name = rename_path(folder)

            try:
                # Rename the folder
                os.rename(folder_path, renamed_folder_path)

                # For compatibility issues, replace all spaces by their encoded alternative
                folder_dict[folder.replace(' ', '%20')] = new_folder_name.replace(' ', '%20')
            except FileExistsError:
                print(f'[WARN] could not rename folder "{folder_path}". (already exists)')

        # Remove trailing IDs from file names and cache them
        for exported_file in files:
            # Create a cache of files and their equivalent without trailing IDs
            renamed_file_path = rename_path(exported_file)
            files_dict[exported_file.replace(' ', '%20')] = renamed_file_path.replace(' ', '%20')

    # Second, we need to iterate again, this time to rename all files and their embedded links
    for (root, dirs, files) in os.walk('data', topdown=True):
        for notion_file in files:
            if notion_file.endswith('.md'):
                # Prepare the location of the file and its new name / path
                file_path = os.path.join(root, notion_file)
                renamed_file_path = rename_path(file_path)

                # Read the content of the file
                with open(file_path, 'r', encoding='UTF-8') as md_file:
                    data = md_file.read()

                # Rename all references to original folders to their new name without ID
                for old_folder, new_folder in folder_dict.items():
                    data = data.replace(old_folder, new_folder)

                # Rename all references to original files to their new name without ID
                for old_file_name, new_file_name in files_dict.items():
                    data = data.replace(old_file_name, new_file_name)

                #data = data.replace('%20', ' ')

                # Write the fixed Markdown file to its correct location
                # then remove the original file from disk
                with open(renamed_file_path, 'w', encoding='UTF-8') as md_file:
                    md_file.write(data)
                os.remove(file_path)

            elif notion_file.endswith('.csv'):
                # Perform similar operation to .md files to .csv databases
                file_path = os.path.join(root, notion_file)
                renamed_file_path = rename_path(file_path)
                if file_path != renamed_file_path:
                    try:
                        os.rename(file_path, renamed_file_path)
                    except FileExistsError:
                        print(f'[WARN] could not rename file "{file_path}". (already exists)')

    print('[INFO] Job finished.')

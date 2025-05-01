from textnode import TextNode
import os
import shutil


def main():

    copy_from_static_to_public()





def copy_from_static_to_public():
    # Get paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    public_dir = os.path.join(project_root, "public")
    static_dir = os.path.join(project_root, "static")
    
    # Remove public directory if it exists
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    
    # Create a fresh public directory
    os.mkdir(public_dir)
    
    # Recursively copy contents from static to public
    copy_directory_recursive(static_dir, public_dir)

def copy_directory_recursive(source, destination):
    # Create destination directory if it doesn't exist
    if not os.path.exists(destination):
        os.mkdir(destination)
    
    # List all items in source directory
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        
        # If it's a file, copy it
        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} to {dest_path}")
            shutil.copy(source_path, dest_path)
        
        # If it's a directory, recursively copy it
        elif os.path.isdir(source_path):
            print(f"Creating directory: {dest_path}")
            # Create the subdirectory in destination
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            # Recursively copy contents of this subdirectory
            copy_directory_recursive(source_path, dest_path)


if __name__ == "__main__":
    main()
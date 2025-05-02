from textnode import TextNode, markdown_to_html_node
import os
import shutil
from htmlnode import HTMLNode
import sys

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"


def main():
    copy_from_static_to_docs()
    generate_pages_recursive(basepath)







def copy_from_static_to_docs():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    docs_dir = os.path.join(project_root, "docs")
    static_dir = os.path.join(project_root, "static")

    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)

    os.mkdir(docs_dir)
    copy_directory_recursive(static_dir, docs_dir)

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

def extract_title(markdown): 
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 header found")
        
def generate_page(from_path, template_path, dest_path, basepath):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        f_path = file.read()
    with open(template_path, 'r') as file:
        t_path = file.read()   

    html_from = markdown_to_html_node(f_path)
    html_string = html_from.to_html()
    
    title_from = extract_title(f_path)
    result = t_path.replace("{{ Title }}", title_from).replace("{{ Content }}", html_string)
    result = result.replace('href="/', f'href="{basepath}')
    result = result.replace('src="/', f'src="{basepath}')

    dir_path = os.path.dirname(dest_path)

    if dir_path: 
        os.makedirs(dir_path, exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(result)

def find_md_files(search_path="content"):
    matches = []
    for dirpath, _, filenames in os.walk(search_path):
        for filename in filenames:
            if filename.endswith(".md"):
                matches.append(os.path.join(dirpath, filename))
    return matches


def generate_pages_recursive(basepath):
    all_paths = find_md_files()
    for path in all_paths:
        dest_path = path.replace("content", "docs").replace(".md", ".html")
        generate_page(path, "template.html", dest_path, basepath)







 

if __name__ == "__main__":
    main()
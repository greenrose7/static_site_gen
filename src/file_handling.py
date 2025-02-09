from os import path, listdir, mkdir, makedirs
from shutil import copy, rmtree
from markdown_blocks import markdown_to_html_node, extract_title

def copy_contents(from_dir, to_dir):
    if path.exists(to_dir):
        rmtree(to_dir)
    mkdir(to_dir)
    for entry in listdir(from_dir):
        current_fullpath = path.join(from_dir, entry)
        dest_fullpath = path.join(to_dir, entry)
        if path.isfile(current_fullpath):
            print(f"Copying {current_fullpath} to {dest_fullpath}")
            copy(current_fullpath, dest_fullpath)
        else:
            mkdir(dest_fullpath)
            copy_contents(current_fullpath, dest_fullpath)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md_file = f.read()
    with open(template_path) as f:
        template_file = f.read()
    print(f"md_file: {md_file}")
    print(f"template_file: {template_file}")
    html_string = markdown_to_html_node(md_file).to_html()
    print(f"html_string: {html_string}")
    title = extract_title(md_file)
    print(f"title: {title}")
    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", html_string)
    print(f"new template: {template_file}")
    if not path.exists(path.dirname(dest_path)):
        makedirs(path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(template_file)
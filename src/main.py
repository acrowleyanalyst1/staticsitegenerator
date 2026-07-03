import os
import shutil
import sys

from blocks import markdown_to_html_node


def copy_static_to_public(source="static", destination="docs"):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)
        else:
            shutil.copy(source_path, destination_path)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise Exception("No title found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html)
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(source_path):
            generate_pages_recursive(source_path, template_path, dest_path, basepath)
        elif item.endswith(".md"):
            html_path = dest_path.replace(".md", ".html")
            generate_page(source_path, template_path, html_path, basepath)


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()

import os
import shutil

from .md_to_html import markdown_to_html_node


class Builder:
    def __init__(self):
        pass

    def __repr__(self):
        return f"Builder({hex(id(self))})"

    def copy_static_to_pub(self, src="./static", dest="./docs"):
        if os.path.exists(dest):
            shutil.rmtree(dest)
        os.mkdir(dest)
        self._copy_recursive(src, dest)

    def _copy_recursive(self, src, dest):
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dest_path = os.path.join(dest, item)
            if os.path.isfile(src_path):
                shutil.copy(src_path, dest_path)
                print(f"Copied: {src_path} -> {dest_path}")
            else:
                os.mkdir(dest_path)
                self._copy_recursive(src_path, dest_path)

    @staticmethod
    def extract_title(markdown: str) -> str:
        for line in markdown.split("\n"):
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
        raise Exception("No h1 header found")

    def generate_page(self, from_path, template_path, dest_path, basepath="/"):
        print(f"Generating page from {from_path} to {dest_path} using {template_path}")

        with open(from_path, "r") as f:
            markdown = f.read()

        with open(template_path, "r") as f:
            template = f.read()

        html_node = markdown_to_html_node(markdown)
        html_content = html_node.to_html()

        title = Builder.extract_title(markdown)

        page = template.replace("{{ Title }}", title)
        page = page.replace("{{ Content }}", html_content)
        page = page.replace('href="/', f'href="{basepath}')
        page = page.replace('src="/', f'src="{basepath}')

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "w") as f:
            f.write(page)

    def generate_pages_recursive(self, dir_path_content, template_path, dest_dir_path, basepath="/"):
        for root, dirs, files in os.walk(dir_path_content):
            for file in files:
                if file.endswith(".md"):
                    from_path = os.path.join(root, file)
                    rel_path = os.path.relpath(from_path, dir_path_content)
                    dest_file = os.path.splitext(rel_path)[0] + ".html"
                    dest_path = os.path.join(dest_dir_path, dest_file)
                    self.generate_page(from_path, template_path, dest_path, basepath)


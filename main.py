import json
from time import strftime, localtime
import markdown
from pathlib import Path

def main():
    input_path = Path("./docs")
    output_path = Path("./dist")

    clear_directory(output_path)
    copy_static_files(output_path)
    markdown_files = list(input_path.glob("**/*.md"))
    navigation_menu, file_metadata = generate_navigation(markdown_files)

    site = load_site_config("./config.yml")

    for file, metadata in file_metadata.items():
        convert_to_html(file, metadata, navigation_menu, input_path, output_path, site)

def load_site_config(config_file):
    site_config = {}
    with open(config_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if ":" in line:
                key, value = map(str.strip, line.split(":", 1))
                site_config[key] = value

    return site_config

def copy_static_files(output_path):
    static_path = Path("./static")
    for file in static_path.glob("*"):
        if file.is_file():
            output_path.joinpath(file.relative_to(static_path)).write_bytes(file.read_bytes())

def clear_directory(output_path):
    for file in output_path.glob("*"):
        if file.is_file():
            file.unlink()

def generate_navigation(files):
    navigation_menu = "<ul>\n"
    file_metadata = {}

    for file in files:
        metadata = extract_metadata(file)
        file_metadata[file] = metadata
        navigation_menu += f'<li><a href="{file.stem}.html">{metadata["title"]}</a></li>\n'

    navigation_menu += "</ul>"
    return navigation_menu, file_metadata

def extract_metadata(file):
    metadata = {"title": file.stem}
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    content_lines = []
    in_metadata_header = True

    for line in lines:
        if ':' in line and in_metadata_header:
            key, value = map(str.strip, line.split(":", 1))
            metadata[key] = value
        elif '---' in line and in_metadata_header:
            in_metadata_header = False
        else:
            content_lines.append(line)
            in_metadata_header = False

    last_modified = file.stat().st_mtime
    metadata["last_modified_date"] = strftime("%Y-%m-%d", localtime(last_modified))
    metadata["last_modified_time"] = strftime("%I:%M %p", localtime(last_modified))
    metadata["content"] = "".join(content_lines)
    return metadata

def convert_to_html(file, metadata, navigation_menu, input_path, output_path, site_config):
    new_file = file.with_suffix(".html").relative_to(input_path)
    search_index = []

    body = markdown.markdown(metadata["content"], extensions=["toc", "tables"])

    with open(output_path / new_file, "w+", encoding="utf-8") as f:
        with open("./template/webpage.html", "r", encoding="utf-8") as template:
            html = template.read()
            html = html.replace("{{style}}", f"{site_config.get('url', '/')}/style.css")
            html = html.replace("{{site_title}}", site_config.get('site_title', 'Documentation'))
            html = html.replace("{{content}}", body)
            html = html.replace("{{title}}", metadata["title"])
            html = html.replace("{{last_modified_time}}", metadata["last_modified_time"])
            html = html.replace("{{last_modified_date}}", metadata["last_modified_date"])
            html = html.replace("{{navigation_menu}}", navigation_menu)
            html = html.replace("{{search_script}}", f"{site_config.get("url", "/")}/search.js")
            f.write(html)
            search_index.append({
                "id": str(file.relative_to(input_path)),
                "title": metadata.get("title", ""),
                "content": metadata["content"],
                "url": f"{new_file.stem}.html"
            })

    update_search_index(search_index, output_path)

def update_search_index(search_index, output_path):
    index_file = output_path / "search_index.json"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.extend(search_index)
    else:
        data = search_index

    with open(index_file, "w+", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4))

if __name__ == "__main__":
    main()

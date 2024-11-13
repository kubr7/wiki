import re, os
import markdown

from . import util

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if not content:
        return None
    else:
        return markdowner.convert(content)


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(
        sorted(
            re.sub(r"\.md$", "", filename)
            for filename in filenames
            if filename.endswith(".md")
        )
    )


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def delete_entry(title):
    """
    Deletes an entry with the given title.
    """
    file_path = get_file_path(title)

    if os.path.exists(file_path):
        os.remove(file_path)


def get_file_path(title):
    """
    Returns the file path for the given entry title.
    """
    return os.path.join("entries", f"{title}.md")

import re


def clean_html(html: str) -> str:
    # Remove images, since they are not useful as markdown.
    # Remove videos, since they are not useful as markdown.
    html = re.sub(r"<video[^>]*>.*?</video>", "", html, flags=re.DOTALL)
    html = re.sub(r"<img[^>]*>", "", html)
    html = re.sub(r"\s+", " ", html)
    return html

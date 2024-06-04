from bs4 import BeautifulSoup
import requests
from markdownify import MarkdownConverter
from markdownify import ATX
import re

# TODO: Fix images
# TODO: Make other links to handbooks work locally??

TITLE_NUM_REGEX = "(\d{1,2}(\.?\d{0,2}){0,3})"


class HandbookConverter(MarkdownConverter):
    def convert_td(self, el, text, convert_as_inline):
        colspan = 1
        if "colspan" in el.attrs:
            colspan = int(el["colspan"])

        # HACK For some reason, LDS.org repeats the header in each row of a table... remove it
        return " " + text.strip().split("\n\n")[-1] + " |" * colspan
        return " " + text.strip().replace("\n", " ") + " |" * colspan


class HandbookDownloader:
    def __init__(self, dir=""):
        self.cache = {}  # map section # to header slug
        self.files = {}  # map filename to markdown
        self.converter = HandbookConverter(heading_style=ATX)

    def cache_headers(self, text, filename):
        # Match of the form "## 1.1.1 Title"
        headers = re.findall(f"(#+) {TITLE_NUM_REGEX} (.*)", text)
        # Cache them to replace links later
        for _, num, _, title in headers:
            # https://stackoverflow.com/a/68227813
            # Create what the link to each header will be
            slug_title = f"{num} {title.lower()}"
            slug_title = re.sub("\s+", "-", slug_title)  # whitespace with -
            slug_title = re.sub(
                "[\]\[\!'\#\$\%\&'\(\)\*\+\,\.\/\:\;\<\=\>\?\@\\\^\_\{\|\}\~\`。，、；：？’]",
                "",
                slug_title,
            )  # remove punctuation
            slug_title = re.sub("^\-+", "", slug_title)  # leading -
            slug_title = re.sub("\-+$", "", slug_title)  # trailing -
            slug_title = f"{filename}#{slug_title}"
            self.cache[num] = slug_title

        num = re.split("[\.-]", filename)[0]
        self.cache[num] = filename

    def add_page(self, url):
        # download page
        filename = url.split("/")[-1] + ".md"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        body = soup.find("div", {"class": "body"})

        # Save & clean title
        header = body.find("header")
        final = self.convert(header)
        final += "\n\n"

        # Save & clean body
        text = body.find("div", {"class": "body-block"})
        text = self.convert(text)
        final += text

        # Get all header, save for link replacement later
        self.cache_headers(final, filename)

        self.files[filename] = final

        return final

    def convert(self, soup):
        text = self.converter.convert_soup(soup).strip()
        text = re.sub(r"\n\s*\n", "\n\n", text)  # remove extra newlines

        # HACK to fix a couple of poor formatting versions from the website
        bad_titles = [
            ("30.8.1", "Ward Callings"),
            ("30.8.2", "Branch Callings"),
            ("30.8.3", "Stake Callings"),
            ("30.8.4", "District Callings"),
        ]
        for num, title in bad_titles:
            text = re.sub(f"{num}\n\n{title}", f"{num}\n\n### {title}", text)

        text = re.sub(
            f"{TITLE_NUM_REGEX}\n\n(#+) (.*)", r"\3 \1 \4", text
        )  # merge number and header (removing trailing dot if needed)
        return text

    def process_links(self):
        # Sanitize all links

        def process(match):
            name = match.group(1).strip()
            link = match.group(2)

            # If it's a chapter link or section number link
            if link.startswith("/study/manual/general-handbook") and (
                num := re.search(TITLE_NUM_REGEX, name)
            ):
                num = num.group(1)
                if num in self.cache:
                    return f"[{name}]({self.cache[num]})"
                else:
                    print(f"Missing num : {name}, {k}")
                    return f"[{name}](https://www.churchofjesuschrist.org{link})"
            # If it's a relative link
            elif link.startswith("/"):
                return f"[{name}](https://www.churchofjesuschrist.org{link})"
            # If it's a valid external link already
            elif link.startswith("http") or link.startswith("mailto"):
                return match.group(0)
            # Empty link TODO: Investigate this more later, also includes the images to change things locally
            elif name == "" or name == "![":
                return ""
            # Otherwise, not sure what it'd be
            else:
                print(f"Unknown link {match.group(0)}, {k}")
                return match.group(0)

        for k in self.files.keys():
            self.files[k] = re.sub(r"\[(.*?)\]\((.*?)\)", process, self.files[k])

    def write_files(self, dir="."):
        # Save all files to a directory
        for k, v in self.files.items():
            with open(f"{dir}/{k}", "w") as f:
                f.write(v)

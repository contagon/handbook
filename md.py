from bs4 import BeautifulSoup
import requests
from markdownify import MarkdownConverter, chomp
from markdownify import ATX, UNDERSCORE
import re

# TODO: Fix images
# TODO: Make other links to handbooks work locally??

TITLE_NUM_REGEX = "(\d{1,2}(\.?\d{0,2}){0,3})"


class HandbookConverter(MarkdownConverter):
    def convert_td(self, el, text, convert_as_inline):
        """Handle tables with bullet points in them via html breaks and bullet points characters"""
        colspan = 1
        if "colspan" in el.attrs:
            colspan = int(el["colspan"])

        text = text.strip().replace("\n", "<br/>")  # replace newlines with breaks
        text = re.sub(r"(?<!\\)\*", "•", text)  # replace asterisks with bullet points

        return " " + text + " |" * colspan

    def convert_img(self, el, text, convert_as_inline):
        """Don't bother with images"""
        return ""

    def convert_a(self, el, text, convert_as_inline):
        """Handle links to adaption/optional resources differently"""
        if not text and el.get("href").startswith(
            "/study/manual/general-handbook/0-introductory-overview"
        ):
            return "[[AO]](0-introductory-overview.md#02-adaptation-and-optional-resources)"

        return super().convert_a(el, text, convert_as_inline)


class HandbookDownloader:
    def __init__(self, dir=""):
        self.cache = {}  # map section # to header slug
        self.files = {}  # map filename to markdown
        self.converter = HandbookConverter(
            heading_style=ATX, strong_em_symbol=UNDERSCORE
        )

    def cache_headers(self, text, filename):
        # Match of the form "## 1.1.1 Title"
        headers = re.findall(f"(#+) {TITLE_NUM_REGEX} (.*)", text)
        # Cache them to replace links to handbook later
        for _, num, _, title in headers:
            # https://stackoverflow.com/a/68227813
            # Create what the link to each header will be
            slug_title = f"{num} {title.lower()}"
            slug_title = re.sub(
                r"\[(.*?)\]\((.*?)\)", r"\1", slug_title
            )  # replace links with their name
            slug_title = re.sub("\s+", "-", slug_title)  # replace whitespace with -
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

        # Get all header info, save for link replacement later
        self.cache_headers(final, filename)

        self.files[filename] = final

        return final

    def convert(self, soup):
        # Remove extra header in body of tables
        for row in soup.find_all("tbody"):
            for extra in row.find_all("p", {"class": "label"}):
                extra.decompose()

        # Remove footnotes
        # To my knowledge, the only page with footnotes is 30.8
        for a in soup.find_all("a", {"class": "note-ref"}):
            a.decompose()

        # Remove images
        for img in soup.select('div[class*="imageWrapper-"]'):
            img.decompose()
        for img in soup.select('span[class*="imageWrapper-"]'):
            img.decompose()

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
            # Link to adapted/optional resources, we handled it earlier
            elif name == "[AO]":
                return match.group(0)
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

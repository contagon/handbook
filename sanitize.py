import re
import os

TITLE_NUM_REGEX = "(\d{1,2}(\.?\d{0,2}){0,3})"


class LinkSanitizer:
    def __init__(self, dir, rm_links) -> None:
        self.dir = dir
        self.rm_links = rm_links
        self.cache = {}  # map section # to header slug
        self.files = {}  # map filename to markdown

        with open("missing.md", "r") as f:
            self.missing = f.read().splitlines()
        self.missing = [
            re.search("/(\d+)[\.\-]", x).group(1)
            for x in self.missing
            if x.startswith(self.dir)
        ]

    def cache_headers(self, text: str, filename: str):
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

    def process_links(self, text, filename):
        file_num = re.split("[\.-]", filename)[0]

        # Sanitize all links
        def process(match):
            name = match.group(1).strip()
            link = match.group(2)

            if self.rm_links:
                return f"[{name}]"

            # If it's a chapter link or section number link
            if link.startswith("/study/manual/general-handbook") and (
                num := re.search(TITLE_NUM_REGEX, name)
            ):
                num = num.group(1)
                if num in self.cache:
                    return f"[{name}]({self.cache[num]})"
                else:
                    # If it's in a missing section, it makes sense it's wrong
                    if (
                        num.split(".")[0] not in self.missing
                        and file_num not in self.missing
                    ):
                        print(f"Missing num : {name}, {filename}")
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
                print(f"Unknown link {match.group(0)}, {filename}")
                return match.group(0)

        return re.sub(r"\[(.*?)\]\((.*?)\)", process, text)

    def run(self):
        # Load in all files
        for filename in os.listdir(self.dir):
            with open(os.path.join(self.dir, filename), "r") as f:
                self.files[filename] = f.read()

        # Cache headers
        for filename, text in self.files.items():
            self.cache_headers(text, filename)

        # Process links
        for k in self.files.keys():
            self.files[k] = self.process_links(self.files[k], k)

        # Resave
        for filename, text in self.files.items():
            with open(os.path.join(self.dir, filename), "w") as f:
                f.write(text)

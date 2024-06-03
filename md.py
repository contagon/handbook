from bs4 import BeautifulSoup
import requests
from markdownify import MarkdownConverter
from markdownify import ATX
import re
from tqdm import tqdm

# TODO: Fix images
# TODO: Make other links to handbooks work locally??

TITLE_NUM_REGEX = "(\d{1,2}(\.?\d{0,2}){0,3})"


class HandbookConverter:
    def __init__(self, dir=""):
        self.cache = {}  # map section # to header slug
        self.files = {}  # map filename to markdown
        self.converter = MarkdownConverter(heading_style=ATX)

    def cache_headers(self, text, filename):
        # Match of the form "## 1.1.1 Title"
        headers = re.findall(f"(#+) {TITLE_NUM_REGEX} (.*)", text)
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
        final = self.md(header)
        final += "\n\n"

        # Save & clean body
        text = body.find("div", {"class": "body-block"})
        text = self.md(text)
        final += text

        # Get all header, save for link replacement later
        self.cache_headers(final, filename)

        self.files[filename] = final

        return final

    def md(self, soup):
        text = self.converter.convert_soup(soup).strip()
        text = re.sub(r"\n\s*\n", "\n\n", text)  # remove extra newlines

        # hack to fix a couple of poor formatting versions from the website
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
        def slug(match):
            name = match.group(1).strip()
            link = match.group(2)

            if name.lower().startswith("chapter"):
                name = re.split("\s", name)[-1]

            # If it's a chapter link or section number link
            if re.fullmatch(TITLE_NUM_REGEX, name) and link.startswith(
                "/study/manual/general-handbook"
            ):
                if name in self.cache:
                    return f"[{name}]({self.cache[name]})"
                else:
                    print(f"Missing num : {name}, {k}")
                    return match.group(0)
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
            self.files[k] = re.sub(r"\[(.*?)\]\((.*?)\)", slug, self.files[k])

    def write_files(self, dir="."):
        for k, v in self.files.items():
            with open(f"{dir}/{k}", "w") as f:
                f.write(v)


urls = [
    "1-work-of-salvation-and-exaltation",
    "2-supporting-individuals-and-families",
    "3-priesthood-principles",
    "4-leadership-in-the-church-of-jesus-christ",
    "5-general-and-area-leadership",
    "6-stake-leadership",
    "7",
    "8-elders-quorum",
    "9-relief-society",
    "10-aaronic-priesthood",
    "11-young-women",
    "12-primary",
    "13-sunday-school",
    "14-single-members",
    "15-seminaries-and-institutes",
    "16-living-the-gospel",
    "17-teaching-the-gospel",
    "18-priesthood-ordinances-and-blessings",
    "19-music",
    "20-activities",
    "21-ministering",
    "22-providing-for-temporal-needs",
    "23",
    "24",
    "25-temple-and-family-history-work",
    "26-temple-recommends",
    "27-temple-ordinances-for-the-living",
    "28",
    "29-meetings-in-the-church",
    "30-callings-in-the-church",
    "31",
    "32-repentance-and-membership-councils",
    "33-records-and-reports",
    "34-finances-and-audits",
    "35",
    "36-creating-changing-and-naming-new-units",
    "37-specialized-stakes-wards-and-branches",
    "38-church-policies-and-guidelines",
]
prefix = "https://www.churchofjesuschrist.org/study/manual/general-handbook/"
urls = [f"{prefix}{u}" for u in urls]

converter = HandbookConverter()

for u in tqdm(urls):
    converter.add_page(u)

converter.process_links()
converter.write_files("handbook")
# from pprint import pprint as print

# print(converter.cache)
